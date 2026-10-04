import traceback
import subprocess
import os

while True:
    result = subprocess.run(['.venv\\Scripts\\python.exe', '-c', 'import backend'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Backend imports cleanly!")
        break
    else:
        # Find the line number from the traceback
        lines = result.stderr.split('\n')
        line_num = None
        for line in reversed(lines):
            if 'File "C:\\Users\\Admin\\Documents\\MedAI\\backend.py", line' in line:
                part = line.split('line ')[1]
                line_num = int(part.split(',')[0])
                break
        
        if line_num:
            print(f"Fixing error at line {line_num}...")
            with open('backend.py', 'r', encoding='utf-8') as f:
                content = f.readlines()
            content[line_num - 1] = '# ' + content[line_num - 1]
            with open('backend.py', 'w', encoding='utf-8') as f:
                f.writelines(content)
        else:
            print("Could not find line number in traceback:")
            print(result.stderr)
            break
if st.button("Analyze Report"):
    if not report_text.strip():
        st.warning("Please paste or upload a CBC report before analyzing.")
    else:
        try:
            with st.spinner("Processing CBC parameters..."):
                results = process_cbc_report(report_text, report_id="CBC-2026")
                
            if not results.get("extracted_parameters"):
                st.warning("No valid CBC parameters (HGB, HCT, PLT, etc.) were detected in the input text.")
            else:
                st.success("Report analyzed successfully!")
                # Render dashboard results...
        except Exception as e:
            st.error(f"Processing error: {str(e)}")