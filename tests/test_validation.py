#!/usr/bin/env python3
"""
Validation tests for Sherbrooke Waste Collection integration.
Checks file structure, imports, and basic logic without running Home Assistant.
Run with: python -m pytest tests/test_validation.py -v
Or standalone: python tests/test_validation.py
"""

import ast
import json
import os
import sys
from pathlib import Path

try:
    import pytest
except ImportError:
    pytest = None


def get_integration_path():
    """Get the path to the integration directory."""
    base_path = Path(__file__).parent.parent
    return base_path / "custom_components" / "sherbrooke_poubelle"


def test_directory_structure():
    """Test that all required files exist."""
    integration_path = get_integration_path()

    assert integration_path.exists(), f"Integration directory not found: {integration_path}"

    required_files = [
        "__init__.py",
        "config_flow.py",
        "const.py",
        "coordinator.py",
        "manifest.json",
        "notify.py",
        "sensor.py",
        "translations/en.json",
        "translations/fr.json",
        "services.yaml",
    ]

    missing = []
    for filename in required_files:
        filepath = integration_path / filename
        if not filepath.exists():
            missing.append(filename)

    assert not missing, f"Missing required files: {missing}"


def test_python_syntax():
    """Test that all Python files have valid syntax."""
    integration_path = get_integration_path()

    python_files = [
        integration_path / "__init__.py",
        integration_path / "config_flow.py",
        integration_path / "const.py",
        integration_path / "coordinator.py",
        integration_path / "notify.py",
        integration_path / "sensor.py",
    ]

    errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            errors.append(f"{py_file.name}: {e}")

    assert not errors, f"Syntax errors found: {errors}"


def test_json_valid():
    """Test that all JSON files are valid."""
    integration_path = get_integration_path()

    json_files = [
        integration_path / "manifest.json",
        integration_path / "translations" / "en.json",
        integration_path / "translations" / "fr.json",
    ]

    errors = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"{json_file.name}: {e}")

    assert not errors, f"JSON errors found: {errors}"


def test_manifest_structure():
    """Test that manifest.json has required fields."""
    integration_path = get_integration_path()
    manifest_file = integration_path / "manifest.json"

    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    required_fields = ['domain', 'name', 'version', 'config_flow']
    missing = [field for field in required_fields if field not in manifest]

    assert not missing, f"Missing manifest fields: {missing}"


def test_domain_consistency():
    """Test that domain is consistent across files."""
    integration_path = get_integration_path()
    const_file = integration_path / "const.py"
    manifest_file = integration_path / "manifest.json"

    # Read DOMAIN from const.py
    with open(const_file, 'r', encoding='utf-8') as f:
        const_content = f.read()

    # Extract DOMAIN value
    domain_line = [line for line in const_content.split('\n') if 'DOMAIN = ' in line]
    assert domain_line, "DOMAIN not found in const.py"

    # Extract the domain value (handle both quotes)
    domain_value = domain_line[0].split('=')[1].strip().strip('"\'')

    # Read domain from manifest.json
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    manifest_domain = manifest.get('domain')

    assert domain_value == manifest_domain, (
        f"Domain mismatch: const.py has '{domain_value}', "
        f"manifest.json has '{manifest_domain}'"
    )


def test_no_debug_prints():
    """Test that no debug print statements remain in production code."""
    integration_path = get_integration_path()

    python_files = [
        integration_path / "__init__.py",
        integration_path / "config_flow.py",
        integration_path / "const.py",
        integration_path / "coordinator.py",
        integration_path / "notify.py",
        integration_path / "sensor.py",
    ]

    debug_prints = []
    for py_file in python_files:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Check for print statements (not logger)
                if 'print(' in line:
                    debug_prints.append(f"{py_file.name}:{i}: {line.strip()}")

    assert not debug_prints, f"Debug print statements found:\n" + '\n'.join(debug_prints)


def test_logger_defined_before_use():
    """Test that _LOGGER is defined before being used."""
    integration_path = get_integration_path()
    config_flow_file = integration_path / "config_flow.py"

    with open(config_flow_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Find first use of _LOGGER and where it's defined
    first_use_line = None
    definition_line = None

    for i, line in enumerate(lines, 1):
        if '_LOGGER' in line:
            if definition_line is None and '_LOGGER =' in line:
                definition_line = i
            elif first_use_line is None and '_LOGGER.' in line:
                first_use_line = i

    # If we found both, check order
    if definition_line and first_use_line:
        assert definition_line < first_use_line, (
            f"_LOGGER used on line {first_use_line} before being defined on line {definition_line}"
        )


def test_coordinator_loop_structure():
    """Test that coordinator.py doesn't have the indentation bug."""
    integration_path = get_integration_path()
    coordinator_file = integration_path / "coordinator.py"

    with open(coordinator_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for the problematic pattern where final_collections is built inside the loop
    # This is a heuristic check - we look for "for event in events:" and then check
    # if "final_collections = []" appears before the next return statement

    lines = content.split('\n')
    in_event_loop = False
    loop_indent = 0
    final_collections_inside_loop = False
    event_loop_start = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if 'for event in events:' in line:
            in_event_loop = True
            loop_indent = indent
            event_loop_start = i
            continue

        if in_event_loop:
            # Check if we've exited the loop (less or equal indent, not empty)
            if indent <= loop_indent and stripped and not stripped.startswith('#'):
                # We've exited the loop, check if return comes after
                break

            # Check for final_collections = [] inside the loop
            if 'final_collections = []' in line and indent > loop_indent:
                final_collections_inside_loop = True

    assert not final_collections_inside_loop, (
        "Indentation bug detected: 'final_collections = []' is inside the 'for event in events:' loop. "
        "This should be outside the loop."
    )


def test_hacs_json_exists():
    """Test that hacs.json exists in root."""
    base_path = Path(__file__).parent.parent
    hacs_file = base_path / "hacs.json"

    assert hacs_file.exists(), "hacs.json not found in repository root"

    with open(hacs_file, 'r', encoding='utf-8') as f:
        hacs = json.load(f)

    assert 'name' in hacs, "hacs.json missing 'name' field"


def test_license_exists():
    """Test that LICENSE file exists."""
    base_path = Path(__file__).parent.parent
    license_file = base_path / "LICENSE"

    assert license_file.exists(), "LICENSE file not found in repository root"


def test_services_yaml_exists():
    """Test that services.yaml exists in integration folder."""
    integration_path = get_integration_path()
    services_file = integration_path / "services.yaml"

    assert services_file.exists(), "services.yaml not found in integration folder"


def test_brand_assets_exist():
    """Test that brand assets exist for HACS submission.

    HACS requires at least icon.png in the brands directory.
    See: https://hacs.xyz/docs/publish/include#brands
    """
    base_path = Path(__file__).parent.parent
    brands_dir = base_path / "custom_components" / "sherbrooke_poubelle" / "brand"

    # Check if brands directory exists inside integration
    if not brands_dir.exists():
        # Also check root-level brands folder
        brands_dir = base_path / "brand"

    icon_file = brands_dir / "icon.png"

    assert icon_file.exists(), (
        f"Brand icon not found at {icon_file}. "
        "HACS requires at least a 256x256px icon.png for custom integrations. "
        "See brands/README.md for details."
    )


def test_brand_icon_is_valid_png():
    """Test that brand icon is a valid PNG file."""
    try:
        from PIL import Image
    except ImportError:
        if pytest:
            pytest.skip("Pillow not installed, skipping image validation")
        else:
            # In standalone mode, just print a warning
            print("\n  Warning: Pillow not installed, skipping PNG validation")
            return

    base_path = Path(__file__).parent.parent
    brands_dir = base_path / "custom_components" / "sherbrooke_poubelle" / "brands"

    if not brands_dir.exists():
        brands_dir = base_path / "brands"

    icon_file = brands_dir / "icon.png"

    if not icon_file.exists():
        if pytest:
            pytest.skip("icon.png not found, skipping PNG validation")
        else:
            print("\n  Warning: icon.png not found, skipping PNG validation")
            return

    try:
        with Image.open(icon_file) as img:
            # Check it's a PNG
            assert img.format == 'PNG', f"Expected PNG format, got {img.format}"

            # Check size
            width, height = img.size
            assert width == 256, f"Expected width 256px, got {width}px"
            assert height == 256, f"Expected height 256px, got {height}px"
    except Exception as e:
        assert False, f"Invalid PNG file: {e}"


# Run standalone if executed directly
if __name__ == "__main__":
    print("=" * 60)
    print("Sherbrooke Waste Collection - Integration Validator")
    print("=" * 60)
    print()

    tests = [
        test_directory_structure,
        test_python_syntax,
        test_json_valid,
        test_manifest_structure,
        test_domain_consistency,
        test_no_debug_prints,
        test_logger_defined_before_use,
        test_coordinator_loop_structure,
        test_hacs_json_exists,
        test_license_exists,
        test_services_yaml_exists,
        test_brand_assets_exist,
        test_brand_icon_is_valid_png,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERR]  {test.__name__}: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All validations passed!")
    else:
        print("Some validations failed. Please fix the errors above.")
        sys.exit(1)
    print("=" * 60)
