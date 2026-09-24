from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace

import mfl_adapter.__main__ as cli


class FakePublication:
    def __init__(self,path,expected_sha):
        self.path=Path(path).resolve()
        self.sha256="master-sha"

    def inventory(self):
        return {"status":"fake-inventory"}

    def unchanged(self):
        return None


def test_build_applies_admission_before_post_plan_and_assembly(
    tmp_path,
    monkeypatch,
):
    master=tmp_path/"master.epub"
    master.write_bytes(b"master")

    profile_path=tmp_path/"profile.json"
    profile_path.write_text(
        "{}",
        encoding="utf-8",
    )

    admission_path=tmp_path/"PLATE_ADMISSION.json"
    admission_path.write_text(
        "{}",
        encoding="utf-8",
    )

    output=tmp_path/"run"

    profile={
        "master_sha256":"expected",
        "reading_document_sha256":"book-sha",
        "_profile_sha256":"profile-sha",
        "components":[
            {
                "key":"plate",
                "route":"SMALL PLATE",
            }
        ],
        "output_epub":"probe.epub",
    }

    monkeypatch.setattr(
        cli,
        "load_profile",
        lambda path:copy.deepcopy(profile),
    )

    monkeypatch.setattr(
        cli,
        "Publication",
        FakePublication,
    )

    monkeypatch.setattr(
        cli,
        "bind_profile",
        lambda pub,p:("doc",[]),
    )

    monkeypatch.setattr(
        cli,
        "plan",
        lambda *args,**kwargs:{"status":"planned"},
    )

    import mfl_adapter.render as render_module
    import mfl_adapter.probe as probe_module
    import mfl_adapter.profile_planning as planning_module
    import mfl_adapter.reproducibility as repro_module
    import mfl_adapter.plate_admission as admission_module

    def fake_render(pub,p,out,chromium):
        plates=out/"plates"
        plates.mkdir()

        (plates/"plate.png").write_bytes(
            b"RGB-BASELINE"
        )

        return {
            "plates":[
                {
                    "key":"plate",
                    "budget_bytes":1000,
                    "optimization":{
                        "selected":"lossless RGB",
                        "selected_bytes":12,
                        "selected_sha256":"baseline",
                    },
                }
            ]
        }

    monkeypatch.setattr(
        render_module,
        "render_plates",
        fake_render,
    )

    post_plan_seen=[]

    def fake_plan_profile(
        profile_path,
        run_dir=None,
        **kwargs,
    ):
        if run_dir is None:
            return {
                "components":[
                    {
                        "key":"plate",
                        "planning_status":"RESERVE MET",
                    }
                ]
            }

        active=(
            Path(run_dir)
            /"plates"
            /"plate.png"
        ).read_bytes()

        post_plan_seen.append(active)

        return {
            "components":[
                {
                    "key":"plate",
                    "planning_status":"RESERVE MET",
                    "byte_status":"WITHIN BUDGET",
                }
            ]
        }

    monkeypatch.setattr(
        planning_module,
        "plan_profile",
        fake_plan_profile,
    )

    monkeypatch.setattr(
        planning_module,
        "require_pre_render_resolved",
        lambda plan:None,
    )

    monkeypatch.setattr(
        planning_module,
        "build_findings",
        lambda plan:[],
    )

    admission_calls=[]

    def fake_apply(
        admission_paths,
        *,
        profile_path,
        run_dir,
        rendering,
    ):
        admission_calls.append(
            list(admission_paths)
        )

        plate=(
            Path(run_dir)
            /"plates"
            /"plate.png"
        )

        assert plate.read_bytes() == b"RGB-BASELINE"

        plate.write_bytes(
            b"ADMITTED-CANDIDATE"
        )

        rendering["plates"][0]["admission"]={
            "status":"ADMITTED"
        }

        rendering["plates"][0]["optimization"]={
            "selected":"admitted palette-256",
            "selected_bytes":18,
            "selected_sha256":"candidate",
        }

        return {
            "schema":"mfl.plate-admissions-applied/1",
            "admission_count":1,
            "admissions":[
                {
                    "component":"plate",
                }
            ],
        }

    monkeypatch.setattr(
        admission_module,
        "apply_plate_admissions",
        fake_apply,
    )

    def fake_assemble(
        pub,p,doc,bindings,out,rendering,
    ):
        active=(
            Path(out)
            /"plates"
            /"plate.png"
        ).read_bytes()

        assert active == b"ADMITTED-CANDIDATE"

        epub=Path(out)/"probe.epub"
        epub.write_bytes(
            b"EPUB-WITH-ADMITTED-CANDIDATE"
        )

        return (
            {
                "mimetype":b"application/epub+zip",
            },
            {"status":"assembled"},
        )

    monkeypatch.setattr(
        probe_module,
        "assemble",
        fake_assemble,
    )

    monkeypatch.setattr(
        probe_module,
        "render_checks",
        lambda *args,**kwargs:{"status":"qa"},
    )

    monkeypatch.setattr(
        repro_module,
        "reproducibility_record",
        lambda *args,**kwargs:{"status":"recorded"},
    )

    monkeypatch.setattr(
        cli,
        "report_text",
        lambda *args,**kwargs:"run record",
    )

    args=SimpleNamespace(
        epub=str(master),
        profile=str(profile_path),
        out=str(output),
        chromium=None,
        admission=[
            str(admission_path),
        ],
    )

    cli.build(args)

    assert admission_calls == [
        [str(admission_path)]
    ]

    assert post_plan_seen == [
        b"ADMITTED-CANDIDATE"
    ]

    admissions=json.loads(
        (
            output
            /"PLATE_ADMISSIONS.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert admissions["admission_count"] == 1

    manifest=json.loads(
        (
            output
            /"MANIFEST.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest["plate_admissions"]["count"]
        == 1
    )

    assert (
        output
        /"plates"
        /"plate.png"
    ).read_bytes() == b"ADMITTED-CANDIDATE"
