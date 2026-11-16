"""
Standalone Test Runner and Execution Reporter for OsdagBridge QA Suite.
Can run under pytest or standard Python unittest runner.
Executes all test modules, calculates execution times, validates assertions,
and prints a formatted QA Execution Summary.
"""

import sys
import time
import inspect
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import test functions from test modules
from tests import test_environment, test_inputs, test_project, test_design, test_reports, test_repository_layout
from osdagbridge_core.models import BridgeProject


class TestFixtureHelper:
    """Provides fixtures dynamically for standalone test execution."""
    @staticmethod
    def project_root():
        return ROOT_DIR

    @staticmethod
    def valid_project_dict():
        import json
        with open(ROOT_DIR / "test_data" / "valid_inputs.json", "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def valid_bridge_project():
        return BridgeProject.from_dict(TestFixtureHelper.valid_project_dict())

    @staticmethod
    def invalid_test_cases():
        import json
        with open(ROOT_DIR / "test_data" / "invalid_inputs.json", "r", encoding="utf-8") as f:
            return json.load(f).get("test_cases", [])

    @staticmethod
    def reference_irc_data():
        import json
        with open(ROOT_DIR / "test_data" / "reference_design_irc.json", "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def tmp_path():
        import tempfile
        return Path(tempfile.mkdtemp())


def run_standalone_suite():
    print("=" * 80)
    print("       OSDAGBRIDGE AUTOMATED QA TEST EXECUTION SUITE")
    print("       Standard IRC:24 / IRC:6 / IS 800:2007 Bridge Verification")
    print("=" * 80)
    print(f"Python Runtime: {sys.version.split()[0]} ({sys.platform})")
    print(f"Working Directory: {ROOT_DIR}\n")

    modules = [
        ("Environment & Layout", test_environment),
        ("Repository Deliverables", test_repository_layout),
        ("Input Validation & Boundaries", test_inputs),
        ("Project Lifecycle & Models", test_project),
        ("Structural Design & IRC Solvers", test_design),
        ("Report Generation & Export", test_reports),
    ]

    fixture_map = {
        "project_root": TestFixtureHelper.project_root,
        "valid_project_dict": TestFixtureHelper.valid_project_dict,
        "valid_bridge_project": TestFixtureHelper.valid_bridge_project,
        "invalid_test_cases": TestFixtureHelper.invalid_test_cases,
        "reference_irc_data": TestFixtureHelper.reference_irc_data,
        "tmp_path": TestFixtureHelper.tmp_path,
    }

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    start_time = time.time()

    for module_name, mod in modules:
        print(f"\n📂 Running Suite: {module_name}")
        print("-" * 60)
        # Find all test_* functions
        funcs = [
            (name, obj) for name, obj in inspect.getmembers(mod, inspect.isfunction)
            if name.startswith("test_")
        ]

        for name, func in funcs:
            total_tests += 1
            sig = inspect.signature(func)
            kwargs = {}
            for param in sig.parameters.values():
                if param.name in fixture_map:
                    kwargs[param.name] = fixture_map[param.name]()

            t0 = time.time()
            try:
                func(**kwargs)
                elapsed = time.time() - t0
                passed_tests += 1
                print(f"  ✅ [PASS] {name} ({elapsed:.3f}s)")
            except Exception as e:
                elapsed = time.time() - t0
                failed_tests += 1
                print(f"  ❌ [FAIL] {name} ({elapsed:.3f}s) -> {e}")

    total_elapsed = time.time() - start_time
    pass_rate = (passed_tests / total_tests * 100.0) if total_tests > 0 else 0.0

    print("\n" + "=" * 80)
    print("                   TEST EXECUTION SUMMARY REPORT")
    print("=" * 80)
    print(f"  Total Test Cases Executed : {total_tests}")
    print(f"  Passed                    : {passed_tests} ✅")
    print(f"  Failed                    : {failed_tests} ❌")
    print(f"  Success / Pass Rate       : {pass_rate:.1f}%")
    print(f"  Total Execution Duration  : {total_elapsed:.3f} seconds")
    print("=" * 80)

    if failed_tests == 0:
        print(" 🎉 ALL AUTOMATED TESTS PASSED! Quality threshold satisfied.")
        return 0
    else:
        print(" ⚠️ SOME TESTS FAILED. Review issues and logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_standalone_suite())
