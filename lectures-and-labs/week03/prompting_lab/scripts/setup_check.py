#!/usr/bin/env python3
"""
Environment Setup Verification Script

Run this if you're having issues with the lab environment.
It will check and fix common setup problems.
"""
import sys
import subprocess
from pathlib import Path

# Colors for output
class C:
    G = "\x1b[32m"  # green
    Y = "\x1b[33m"  # yellow
    R = "\x1b[31m"  # red
    B = "\x1b[34m"  # blue
    D = "\x1b[0m"   # reset
    BOLD = "\x1b[1m"

ROOT = Path(__file__).resolve().parents[1]

def check_python():
    """Check Python version and interpreter location."""
    print(f"🐍 Python executable: {C.B}{sys.executable}{C.D}")
    print(f"🐍 Python version: {C.B}{sys.version}{C.D}")
    
    if sys.version_info >= (3, 10):
        print(f"   {C.G}✅ Python version is compatible{C.D}")
        return True
    else:
        print(f"   {C.R}❌ Python 3.10+ required{C.D}")
        return False

def check_pip():
    """Check if pip is working."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print(f"📦 {C.G}✅ pip is working{C.D}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"📦 {C.R}❌ pip is not working properly{C.D}")
        print(f"📦 {C.Y}Trying to install pip...{C.D}")
        try:
            # Try to install pip using ensurepip
            subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                          check=True, capture_output=True)
            print(f"📦 {C.G}✅ pip installed successfully{C.D}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"📦 {C.R}❌ Failed to install pip{C.D}")
            return False

def check_requirements():
    """Check if required packages are installed."""
    required_packages = ["pytest"]
    missing = []
    
    for package in required_packages:
        try:
            # Try importing in a subprocess to use the same Python environment
            result = subprocess.run([sys.executable, "-c", f"import {package}"], 
                                  capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            if result.returncode == 0:
                print(f"📚 {C.G}✅ {package} is installed{C.D}")
            else:
                print(f"📚 {C.Y}⚠️  {package} is missing{C.D}")
                missing.append(package)
        except (OSError, FileNotFoundError):
            print(f"📚 {C.Y}⚠️  {package} is missing{C.D}")
            missing.append(package)
    
    return missing

def install_requirements():
    """Install missing requirements."""
    print(f"\n{C.BOLD}🔧 Installing requirements...{C.D}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(f"{C.G}✅ Requirements installed successfully{C.D}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{C.R}❌ Failed to install requirements:{C.D}")
        print(f"   {e.stderr}")
        return False

def check_lab_structure():
    """Check if lab directory structure exists."""
    required_dirs = ["lab", "lab/prompts", "lab/code", "lab/tests", "lab/diffs"]
    required_files = ["lab/code/domains.py", "lab/code/batches.py", "lab/tests/test_extract_domain.py"]
    
    print("\n📁 Checking lab structure...")
    all_good = True
    
    for dir_path in required_dirs:
        full_path = ROOT / dir_path
        if full_path.exists():
            print(f"   {C.G}✅ {dir_path}/{C.D}")
        else:
            print(f"   {C.Y}⚠️  {dir_path}/ (missing){C.D}")
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"   {C.G}✅ Created {dir_path}/{C.D}")
    
    for file_path in required_files:
        full_path = ROOT / file_path
        if full_path.exists():
            print(f"   {C.G}✅ {file_path}{C.D}")
        else:
            print(f"   {C.Y}⚠️  {file_path} (missing){C.D}")
            all_good = False
    
    return all_good

def main():
    print(f"{C.BOLD}{C.B}🔍 Lab Environment Setup Check{C.D}")
    print("=" * 40)
    
    all_checks_passed = True
    
    # Check Python
    if not check_python():
        all_checks_passed = False
    
    # Check pip
    if not check_pip():
        all_checks_passed = False
    
    # Check and install requirements
    missing_packages = check_requirements()
    if missing_packages:
        if install_requirements():
            # Re-check after installation
            missing_packages = check_requirements()
            if missing_packages:
                all_checks_passed = False
        else:
            all_checks_passed = False
    
    # Check lab structure
    if not check_lab_structure():
        print(f"\n{C.Y}ℹ️  Some lab files are missing - this is normal for a new lab{C.D}")
    
    print(f"\n{'='*40}")
    if all_checks_passed:
        print(f"{C.G}{C.BOLD}🎉 Environment setup is complete!{C.D}")
        print(f"\nYou can now run: {C.B}python scripts/check_progress.py{C.D}")
    else:
        print(f"{C.R}{C.BOLD}❌ Some setup issues found{C.D}")
        print("\nPlease fix the issues above and run this script again.")
        print("\nIf problems persist, try:")
        print(f"  {C.B}pip install --upgrade pip{C.D}")
        print(f"  {C.B}pip install -r requirements.txt{C.D}")
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    raise SystemExit(main())