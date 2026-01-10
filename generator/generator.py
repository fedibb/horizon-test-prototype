#!/usr/bin/env python3
"""
Horizon Test Generator
Generates pytest test files from Codebeamer requirements using Jinja2 templates
"""

import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


class HorizonTestGenerator:
    """
    Test Generator for Horizon Connect
    
    Reads requirements from mock Codebeamer JSON
    Selects appropriate Jinja2 template based on test_type
    Generates pytest test files with full traceability
    """
    
    def __init__(self, requirements_file, templates_dir, output_dir):
        self.requirements_file = Path(requirements_file)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Template mapping
        self.template_map = {
            "esim_profile_download": "esim_profile_download.j2",
            "network_registration": "network_registration.j2"
        }
    
    def load_requirements(self):
        """Load requirements from JSON file"""
        with open(self.requirements_file, 'r') as f:
            data = json.load(f)
        return data['requirements']
    
    def select_template(self, requirement):
        """
        Select appropriate Jinja2 template based on test_type
        
        This is the core logic that maps requirements to templates:
        - test_type field determines which template to use
        - One template can handle many similar requirements
        - Templates = Patterns, Not Requirements
        """
        test_type = requirement.get('test_type')
        
        if test_type not in self.template_map:
            raise ValueError(f"Unknown test_type: {test_type}")
        
        return self.template_map[test_type]
    
    def generate_test(self, requirement):
        """Generate a single test file from requirement"""
        
        # Select template
        template_name = self.select_template(requirement)
        template = self.jinja_env.get_template(template_name)
        
        # Render template with requirement data
        test_code = template.render(requirement=requirement)
        
        # Generate output filename
        req_id = requirement['id'].lower().replace('-', '_')
        output_file = self.output_dir / f"test_{req_id}.py"
        
        # Write test file
        with open(output_file, 'w') as f:
            f.write(test_code)
        
        return output_file
    
    def generate_all(self):
        """Generate tests for all requirements"""
        requirements = self.load_requirements()
        
        print("=" * 60)
        print("HORIZON TEST GENERATOR")
        print("=" * 60)
        print(f"Requirements file: {self.requirements_file}")
        print(f"Templates directory: {self.templates_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Total requirements: {len(requirements)}")
        print("=" * 60)
        
        generated_tests = []
        
        for req in requirements:
            print(f"\nProcessing: {req['id']} - {req['title']}")
            print(f"  Test Type: {req['test_type']}")
            print(f"  Priority: {req['priority']}")
            
            try:
                output_file = self.generate_test(req)
                generated_tests.append({
                    'requirement_id': req['id'],
                    'test_file': str(output_file),
                    'test_type': req['test_type'],
                    'status': 'success'
                })
                print(f"  ✓ Generated: {output_file.name}")
                
            except Exception as e:
                generated_tests.append({
                    'requirement_id': req['id'],
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"  ✗ Failed: {e}")
        
        # Generate summary
        print("\n" + "=" * 60)
        print("GENERATION SUMMARY")
        print("=" * 60)
        
        success_count = sum(1 for t in generated_tests if t['status'] == 'success')
        print(f"✓ Successfully generated: {success_count}/{len(requirements)}")
        print(f"✗ Failed: {len(requirements) - success_count}")
        
        # Save generation report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_requirements': len(requirements),
            'generated_tests': generated_tests,
            'success_rate': f"{(success_count/len(requirements)*100):.1f}%"
        }
        
        report_file = self.output_dir / 'generation_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nGeneration report: {report_file}")
        print("=" * 60)
        
        return generated_tests


def main():
    """Main entry point"""
    
    # Paths
    base_dir = Path(__file__).parent.parent
    requirements_file = base_dir / "mock_codebeamer" / "requirements.json"
    templates_dir = base_dir / "generator" / "templates"
    output_dir = base_dir / "tests"
    
    # Create generator
    generator = HorizonTestGenerator(
        requirements_file=requirements_file,
        templates_dir=templates_dir,
        output_dir=output_dir
    )
    
    # Generate all tests
    generator.generate_all()


if __name__ == "__main__":
    main()
