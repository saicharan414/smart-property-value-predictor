#!/usr/bin/env python3
"""
Test Runner for Smart Property Value Predictor

This script provides easy ways to run tests with different options:
- Run all tests
- Run specific test classes
- Generate coverage reports
- Run performance tests
"""

import sys
import os
import unittest
import argparse
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests(verbosity=2):
    """Run all test cases"""
    print(f"🧪 Running All Tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Import test module
    from test_spvp import SPVPTestCase, TestUserAuthentication, TestPropertyPrediction
    from test_spvp import TestAdminFunctionality, TestCSVUploadAndTraining, TestErrorHandling
    from test_spvp import TestModelValidation, TestSecurity, TestPerformance
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestUserAuthentication,
        TestPropertyPrediction, 
        TestAdminFunctionality,
        TestCSVUploadAndTraining,
        TestErrorHandling,
        TestModelValidation,
        TestSecurity,
        TestPerformance
    ]
    
    total_tests = 0
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
        total_tests += tests.countTestCases()
    
    print(f"📊 Total Tests: {total_tests}")
    print("=" * 80)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"🚫 Errors: {len(result.errors)}")
    print(f"⏱️  Time: {result.timeTaken:.2f} seconds")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n🚫 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()

def run_specific_tests(test_class_names, verbosity=2):
    """Run specific test classes"""
    print(f"🧪 Running Specific Tests: {', '.join(test_class_names)}")
    print("=" * 80)
    
    from test_spvp import SPVPTestCase
    
    test_suite = unittest.TestSuite()
    
    for class_name in test_class_names:
        try:
            test_class = globals()[class_name]
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            test_suite.addTests(tests)
            print(f"✅ Added {class_name}: {tests.countTestCases()} tests")
        except KeyError:
            print(f"❌ Test class not found: {class_name}")
    
    if test_suite.countTestCases() == 0:
        print("❌ No valid test classes found!")
        return False
    
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    result = runner.run(test_suite)
    
    print(f"\n📊 Results: {result.testsRun - len(result.failures) - len(result.errors)} passed, "
          f"{len(result.failures)} failed, {len(result.errors)} errors")
    
    return result.wasSuccessful()

def run_quick_tests():
    """Run quick tests (excluding performance and integration tests)"""
    print("🚀 Running Quick Tests (Core Functionality)")
    print("=" * 80)
    
    from test_spvp import TestUserAuthentication, TestPropertyPrediction, TestErrorHandling
    
    test_suite = unittest.TestSuite()
    
    quick_test_classes = [
        TestUserAuthentication,
        TestPropertyPrediction,
        TestErrorHandling
    ]
    
    for test_class in quick_test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    print(f"\n⚡ Quick Tests: {result.testsRun - len(result.failures) - len(result.errors)} passed, "
          f"{len(result.failures)} failed, {len(result.errors)} errors")
    
    return result.wasSuccessful()

def generate_test_report():
    """Generate a detailed test report"""
    print("📝 Generating Test Report...")
    
    # Create report file
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_file, 'w') as f:
        f.write("Smart Property Value Predictor - Test Report\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Run tests and capture output
        import io
        from contextlib import redirect_stdout
        
        captured_output = io.StringIO()
        
        # Redirect stdout to capture test output
        with redirect_stdout(captured_output):
            success = run_all_tests(verbosity=2)
        
        # Write captured output to report
        f.write(captured_output.getvalue())
        
        f.write(f"\n\nOverall Result: {'SUCCESS' if success else 'FAILURE'}\n")
    
    print(f"📄 Test report saved to: {report_file}")
    return report_file

def main():
    """Main test runner with command line arguments"""
    parser = argparse.ArgumentParser(description='Test Runner for Smart Property Value Predictor')
    parser.add_argument('--quick', action='store_true', help='Run quick tests only')
    parser.add_argument('--report', action='store_true', help='Generate detailed test report')
    parser.add_argument('--classes', nargs='+', help='Run specific test classes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet output')
    
    args = parser.parse_args()
    
    # Set verbosity
    if args.verbose:
        verbosity = 2
    elif args.quiet:
        verbosity = 0
    else:
        verbosity = 1
    
    print("🧪 Smart Property Value Predictor Test Runner")
    print("=" * 60)
    
    success = True
    
    try:
        if args.classes:
            success = run_specific_tests(args.classes, verbosity)
        elif args.quick:
            success = run_quick_tests()
        else:
            success = run_all_tests(verbosity)
        
        if args.report:
            generate_test_report()
        
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        success = False
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        success = False
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
