from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib_fontja  # noqa: F401
import datetime
from pydantic import BaseModel
import json
from pathlib import Path
import sys
import gc
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent / "speed_test"))
from app import lambda_handler  # noqa

PROCESS_COUNT_REQUESTS = 10
PROCESS_COLOR = "#0972d3"

PROCESSING = [
    pytest.param("subinterpreter"),
    pytest.param("threads"),
    pytest.param("async"),
    pytest.param("single"),
    pytest.param("subprocess"),
    pytest.param("subinterpreter_subproc"),
    pytest.param("subinterpreter_threads"),
]


class CustomMethodformatter(ticker.Formatter):
    def __init__(self):
        pass

    def __call__(self, x, pos=None):
        return datetime.datetime.fromtimestamp(x).strftime("%M:%S")


class DateSpan(BaseModel):
    start: float
    end: float

    @staticmethod
    def from_log_data(log_data: dict):
        elapsed_time = log_data.get("elapsed_time", "0.0")
        start_delta = log_data.get("start_delta", "0.0")
        return DateSpan(
            start=float(start_delta), end=float(start_delta) + float(elapsed_time)
        )

    @property
    def data(self):
        return [self.start, self.start, self.end, self.end]


def _execute_visualize(
    target, capfd, process, ax_fig, ax_label, display_text: str, process_counts: int
):
    lambda_handler(
        {
            "body": json.dumps(
                {
                    "request_id": "test",
                    "target": process,
                    "type": target,
                    "process_count": process_counts,
                }
            )
        },
        None,
    )
    gc.collect()

    if capfd is None:
        return

    out, err = capfd.readouterr()

    if len(out) == 0:
        return

    show_data = []
    label_data = []
    duration = 0.0
    process_name = ""
    module_name = ""
    date_time = ""
    result_text = ""
    index_name = 1

    out: str
    for line in out.split("\n"):
        if line.startswith("{"):
            try:
                data = json.loads(line)
                if "duration" in data:
                    duration = float(data["duration"])
                    process_name = data["processing"]
                    module_name = data["module_name"]
                    date_time = data["start"]
                    result_text = data["result"]

                elif "elapsed_time" in data:
                    insert_data = DateSpan.from_log_data(data).data
                    insert_label = f"{index_name}"
                    show_data.insert(0, insert_data)
                    label_data.insert(0, insert_label)
                    index_name += 1
            except Exception:
                pass

    ax_fig.boxplot(
        x=show_data,
        notch=0,
        sym="rs",
        vert=False,
        labels=label_data,
        patch_artist=True,
        boxprops=dict(
            facecolor=PROCESS_COLOR,
            color=PROCESS_COLOR,
            linewidth=1,
        ),
        medianprops=dict(color=PROCESS_COLOR, linewidth=1),
        whiskerprops=dict(color=PROCESS_COLOR, linewidth=1),
        capprops=dict(color=PROCESS_COLOR, linewidth=1),
        flierprops=dict(markeredgecolor=PROCESS_COLOR, markeredgewidth=1),
    )

    ax_fig.xaxis.set_major_formatter(CustomMethodformatter())
    ax_fig.set_xlim(0, duration)
    ax_fig.set_xlabel(module_name)

    LINE_Y_BEGIN = 1.0 - 0.1
    LINE_SKIP = 0.1
    X_PADDING = 0.1
    TEXTS = [
        f"対象処理: {display_text}",
        f"処理方法: {process_name}",
        f"実行時間: {duration}秒",
        f"同時実行: {process_counts}件",
        f"実施時間: {date_time}",
        f"実施結果: {result_text}",
    ]
    for i, t in enumerate(TEXTS):
        ax_label.text(X_PADDING, LINE_Y_BEGIN - LINE_SKIP * i, t)

    ax_label.spines["top"].set_visible(False)
    ax_label.spines["right"].set_visible(False)
    ax_label.spines["bottom"].set_visible(False)
    ax_label.spines["left"].set_visible(False)
    ax_label.axes.get_xaxis().set_visible(False)
    ax_label.axes.get_yaxis().set_visible(False)


def _execute_test_by_process(
    capfd, process: str, display_text: str, process_counts: int
):
    for target_ in PROCESSING:
        target = target_.values[0]
        file_name = str(Path("images") / f"{target}-{process}.png")
        fig, ax = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
        _execute_visualize(
            target, capfd, process, ax[0, 0], ax[0, 1], display_text, process_counts
        )
        file_name = str(Path("images") / f"{target}-{process}.png")
        plt.savefig(file_name)
        image = Image.open(file_name)
        image.crop((0, 0, image.width, int(image.height / 2))).save(file_name)


def _test_local(capfd):
    _execute_test_by_process(
        capfd, "local", "フィボナッチ数列の計算", PROCESS_COUNT_REQUESTS
    )


def _test_sleep(capfd):
    _execute_test_by_process(capfd, "sleep", "スリープ処理", PROCESS_COUNT_REQUESTS)


def _test_curl(capfd):
    _execute_test_by_process(capfd, "curl", "HTTPリクエスト", PROCESS_COUNT_REQUESTS)


def _test_sts(capfd):
    _execute_test_by_process(
        capfd, "sts", "Boto3 STSリクエスト", PROCESS_COUNT_REQUESTS
    )


def test_curl_sts(capfd):
    _execute_test_by_process(
        capfd, "curl_sts", "HTTP STSリクエスト", PROCESS_COUNT_REQUESTS
    )
