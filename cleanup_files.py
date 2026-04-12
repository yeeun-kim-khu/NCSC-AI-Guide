import os

# 삭제할 파일 목록
files_to_delete = [
    # Old app
    "app.py",
    
    # CSV/Excel test files
    "csv_to_rag.py", "csv_to_rag_final.py", "csv_to_rag_fixed.py",
    "direct_csv_processor.py", "direct_csv_read.py", "direct_csv_reader.py",
    "direct_excel.py", "direct_excel_simple.py", "direct_excel_test.py",
    "excel_rag_converter.py", "excel_reader.py", "excel_reader_final.py", "excel_to_rag.py",
    "extract_csv_data.py", "manual_csv_add.py", "manual_csv_read.py", "manual_excel_processor.py",
    "process_excel_data.py", "quick_csv_test.py", "read_actual_csv.py", "read_excel_data.py", "read_excel_files.py",
    "simple_csv_converter.py", "simple_csv_reader.py", "simple_csv_test.py", "simple_excel_read.py", "simple_extract.py",
    
    # Old RAG versions
    "rag_fixed_final.py", "rag_new.py", "rag_optimized.py", "hybrid_rag.py", "manual_rag_fix.py",
    
    # Test scripts
    "test_csv_load.py", "test_csv_output.py", "test_csv_simple.py", "test_multilingual.py",
    "test_notice.py", "test_rag_search.py", "test_read.py", "quick_test.py",
    
    # Debug scripts
    "debug_notice.py", "debug_rag.py", "check_files.py", "file_finder.py", "fix_csv_paths.py",
    
    # Other
    "add_new_exhibit.py", "new_exhibit_template.txt", "README_complete.html", "0322.code-workspace",
    "cleanup.bat"
]

deleted_count = 0
not_found_count = 0

for filename in files_to_delete:
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"✅ Deleted: {filename}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Error deleting {filename}: {e}")
    else:
        not_found_count += 1

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Deleted: {deleted_count} files")
print(f"  Not found: {not_found_count} files")
print(f"{'='*60}")
