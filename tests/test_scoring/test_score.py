import numpy as np
import pytest

from mbqs.scoring.score import MBQS, TestSuccess, compute_score, compute_test_success

ATOL = 1e-4
J_75 = 1.2160498936625515

samples = {
    3: {
        "000": 665,
        "111": 343,
        "100": 180,
        "010": 179,
        "001": 176,
        "101": 154,
        "011": 152,
        "110": 151,
    }
}

exact_corr = {
    3: {
        (0, 1): 0.4134,
    },
    4: {
        (0, 1): 0.4212,
        (0, 2): 0.4189,
    },
    5: {
        (0, 1): 0.4393,
        (0, 2): 0.4106,
    },
    6: {
        (0, 1): 0.4814,
        (0, 2): 0.3823,
        (0, 3): 0.4981,
    },
    7: {
        (0, 1): 0.4987,
        (0, 2): 0.3709,
        (0, 3): 0.4564,
    },
    8: {
        (0, 1): 0.4888,
        (0, 2): 0.3435,
        (0, 3): 0.3846,
        (0, 4): 0.4429,
    },
}

exact_expected = {
    3: {"metric": 0.0, "success": TestSuccess.SUCCESS},
    4: {"metric": 0.0, "success": TestSuccess.SUCCESS},
    5: {"metric": 0.0, "success": TestSuccess.SUCCESS},
    6: {"metric": 0.0, "success": TestSuccess.SUCCESS},
    7: {"metric": 0.0, "success": TestSuccess.SUCCESS},
    8: {"metric": 0.0, "success": TestSuccess.SUCCESS},
}

approx_corr = {
    3: {
        (0, 1): 0.4,
    },
    4: {
        (0, 1): 0.4,
        (0, 2): 0.38,
    },
    5: {
        (0, 1): 0.41,
        (0, 2): 0.36,
    },
    6: {
        (0, 1): 0.44,
        (0, 2): 0.34,
        (0, 3): 0.43,
    },
    7: {
        (0, 1): 0.47,
        (0, 2): 0.34,
        (0, 3): 0.41,
    },
    8: {
        (0, 1): 0.4,
        (0, 2): 0.29,
        (0, 3): 0.31,
        (0, 4): 0.4,
    },
}

approx_expected = {
    3: {"metric": 0.03241616266811346, "success": TestSuccess.SUCCESS},
    4: {"metric": 0.07168216691358406, "success": TestSuccess.SUCCESS},
    5: {"metric": 0.0948820056849678, "success": TestSuccess.SUCCESS},
    6: {"metric": 0.11111606000822583, "success": TestSuccess.FAILED},
    7: {"metric": 0.08079811454669417, "success": TestSuccess.SUCCESS},
    8: {"metric": 0.15709196923017987, "success": TestSuccess.FAILED},
}

approx_expected_err = {
    3: {"metric": 0.03241616266811346, "success": TestSuccess.SUCCESS},
    4: {"metric": 0.07168216691358406, "success": TestSuccess.SUCCESS},
    5: {"metric": 0.0948820056849678, "success": TestSuccess.UNDECIDED},
    6: {"metric": 0.11111606000822583, "success": TestSuccess.FAILED},
    7: {"metric": 0.08079811454669417, "success": TestSuccess.SUCCESS},
    8: {"metric": 0.15709196923017987, "success": TestSuccess.FAILED},
}


@pytest.mark.parametrize(
    ("metric", "threshold", "expected"),
    [
        (0.05, 0.1, TestSuccess.SUCCESS),
        (0.15, 0.1, TestSuccess.FAILED),
        (0.1, 0.1, TestSuccess.UNDECIDED),
    ],
)
def test_compute_test_success(
    metric: float, threshold: float, expected: TestSuccess
) -> None:
    """
    Test compute_test_success comparison.
    """
    assert compute_test_success(metric, threshold=threshold) is expected


@pytest.mark.parametrize(
    ("metric", "metric_err", "threshold", "expected"),
    [
        (0.05, 0.01, 0.1, TestSuccess.SUCCESS),
        (0.05, 0.05, 0.1, TestSuccess.UNDECIDED),
        (0.05, 0.2, 0.1, TestSuccess.UNDECIDED),
        (0.15, 0.2, 0.1, TestSuccess.FAILED),
        (0.1, 0.2, 0.1, TestSuccess.UNDECIDED),
    ],
)
def test_compute_test_success_with_err(
    metric: float, metric_err: float, threshold: float, expected: TestSuccess
) -> None:
    """
    Test compute_test_success comparison.
    """
    assert compute_test_success(metric, metric_err, threshold=threshold) is expected


@pytest.mark.parametrize(
    ("metric", "threshold", "expected"),
    [
        (0.05, [0.1, 0.2], {0.1: TestSuccess.SUCCESS, 0.2: TestSuccess.SUCCESS}),
        (0.15, [0.1, 0.2], {0.1: TestSuccess.FAILED, 0.2: TestSuccess.SUCCESS}),
        (0.1, [0.1, 0.2], {0.1: TestSuccess.UNDECIDED, 0.2: TestSuccess.SUCCESS}),
    ],
)
def test_compute_test_success_list(
    metric: float, threshold: list[float], expected: dict[float, TestSuccess]
) -> None:
    """
    Test compute_test_success comparison.
    """
    assert compute_test_success(metric, threshold=threshold) == expected


@pytest.mark.parametrize(
    ("correlations", "expected_score", "expected_history"),
    [
        (exact_corr, 8, exact_expected),
        (approx_corr, 5, approx_expected),
    ],
)
def test_compute_score_correlations(
    correlations, expected_score, expected_history
) -> None:

    threshold = 0.1

    score, history = compute_score(
        correlations, J=J_75, state="down", threshold=threshold
    )

    assert score == expected_score
    assert len(history) == len(expected_history)

    for L, values in history.items():
        assert np.isclose(values["metric"], expected_history[L]["metric"], atol=ATOL)
        assert values["success"] == expected_history[L]["success"]


def test_compute_score_correlations_err() -> None:

    threshold = 0.1
    err = 0.008

    expected_score = 4

    correlations_errors = {
        L: {k: err for k in corr.keys()} for L, corr in approx_corr.items()
    }

    score, history = compute_score(
        approx_corr, correlations_errors, J=J_75, state="down", threshold=threshold
    )

    assert score == expected_score
    assert len(history) == len(approx_expected_err)

    for L, values in history.items():
        assert np.isclose(values["metric"], approx_expected_err[L]["metric"], atol=ATOL)
        assert values["success"] == approx_expected_err[L]["success"]


def test_compute_score_correlations_list() -> None:

    thresholds = [0.1, 0.15]

    correlations = approx_corr

    expected_success = {
        3: {0.1: TestSuccess.SUCCESS, 0.15: TestSuccess.SUCCESS},
        4: {0.1: TestSuccess.SUCCESS, 0.15: TestSuccess.SUCCESS},
        5: {0.1: TestSuccess.SUCCESS, 0.15: TestSuccess.SUCCESS},
        6: {0.1: TestSuccess.FAILED, 0.15: TestSuccess.SUCCESS},
        7: {0.1: TestSuccess.SUCCESS, 0.15: TestSuccess.SUCCESS},
        8: {0.1: TestSuccess.FAILED, 0.15: TestSuccess.FAILED},
    }

    expected_score = {0.1: 5, 0.15: 7}

    score, history = compute_score(
        correlations, J=J_75, state="down", threshold=thresholds
    )

    assert score == expected_score
    for L, values in history.items():
        assert values["success"] == expected_success[L]


@pytest.mark.parametrize(
    ("err", "expected_score"),
    [
        (0.0, 5),
        (0.008, 4),
    ],
)
def test_compute_score_stop_on_fail(err, expected_score) -> None:
    """
    Test compute_score stop_on_fail parameter.
    """

    threshold = 0.1

    correlations = approx_corr

    correlations_errors = {
        L: {k: err for k in corr.keys()} for L, corr in correlations.items()
    }

    score, history = compute_score(
        correlations,
        correlations_errors,
        J=J_75,
        state="down",
        threshold=threshold,
        stop_on_fail=True,
    )

    assert score == expected_score
    assert len(history) == expected_score - 1
    assert expected_score + 2 not in history


def test_mbqs_class_init_correlations() -> None:
    """
    Test MBQS class initialization with correlations.
    """

    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=0.1)

    assert mbqs.J == J_75
    assert mbqs.state == "down"
    assert mbqs.threshold == 0.1
    assert mbqs.correlations == approx_corr


def test_mbqs_class_init_samples() -> None:
    """
    Test MBQS class initialization with samples.
    """

    mbqs = MBQS(data=samples, J=J_75, state="down", threshold=0.1)

    assert mbqs.J == J_75
    assert mbqs.state == "down"
    assert mbqs.threshold == 0.1
    assert mbqs.correlations == {3: {(0, 1): np.float64(0.3083916666666667)}}


def test_mbqs_class_compute_score() -> None:
    """
    Test MBQS class compute_score method.
    """

    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=0.1)
    mbqs.compute_score()

    assert mbqs.score == 5
    assert mbqs.history == approx_expected


def test_mbqs_class_extract_array() -> None:
    """
    Test MBQS class extract_array method.
    """

    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=0.1)
    mbqs.compute_score()

    assert mbqs.history is not None

    assert np.allclose(
        mbqs.extract_array("metric"),
        np.array([values["metric"] for values in mbqs.history.values()]),
    )
    assert np.array_equal(
        mbqs.extract_array("success"),
        np.array([float(values["success"]) for values in mbqs.history.values()]),
    )


def test_mbqs_summary() -> None:
    """
    Test MBQS summary method.
    """

    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=0.1)
    mbqs.compute_score()

    summary = mbqs.summary()
    assert summary["J"] == J_75
    assert summary["state"] == "down"
    assert summary["threshold"] == 0.1
    assert summary["score"] == 5
    assert summary["history"] == approx_expected


def test_mbqs_extract_array_errors() -> None:
    """
    Test MBQS extract_array error cases.
    """

    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=0.1)

    with pytest.raises(ValueError, match="No history computed yet."):
        mbqs.extract_array("metric")

    mbqs.compute_score()
    with pytest.raises(ValueError, match="Invalid key: invalid"):
        mbqs.extract_array("invalid")


def test_mbqs_extract_array_multiple_thresholds() -> None:
    """
    Test MBQS extract_array with multiple thresholds.
    """

    thresholds = [0.1, 0.15]
    mbqs = MBQS(data=approx_corr, J=J_75, state="down", threshold=thresholds)
    mbqs.compute_score()

    success_arr = mbqs.extract_array("success")
    assert success_arr.shape == (6, 2)
