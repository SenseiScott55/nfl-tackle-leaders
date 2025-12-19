"""
Package Lambda functions with dependencies
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def package_lambda(function_dir: str):
    """Package a Lambda function with its dependencies"""
    function_path = Path(function_dir)
    function_name = function_path.name
    
    print(f"\n📦 Packaging {function_name}...")
    
    # Create package directory
    package_dir = function_path / "package"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Install dependencies
    requirements_file = function_path / "requirements.txt"
    if requirements_file.exists():
        print(f"   Installing dependencies from {requirements_file}...")
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "-r", str(requirements_file),
            "-t", str(package_dir),
            "--quiet"
        ], check=True)
    
    # Copy function code
    print(f"   Copying function code...")
    for file in function_path.glob("*.py"):
        shutil.copy(file, package_dir)
    
    # Create zip file
    zip_path = function_path / f"{function_name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    
    print(f"   Creating {zip_path}...")
    shutil.make_archive(
        str(zip_path.with_suffix('')),
        'zip',
        str(package_dir)
    )
    
    # Cleanup
    shutil.rmtree(package_dir)
    
    print(f"   ✅ Created {zip_path}")
    return zip_path

if __name__ == "__main__":
    # Package both Lambda functions
    lambda_dir = Path(__file__).parent.parent / "lambda"
    
    ingest_zip = package_lambda(lambda_dir / "ingest")
    api_zip = package_lambda(lambda_dir / "api")
    
    print("\n✅ All Lambda functions packaged!")
    print(f"   Ingest: {ingest_zip}")
    print(f"   API: {api_zip}")