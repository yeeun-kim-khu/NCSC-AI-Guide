@echo off
echo Cleaning up unnecessary files...

REM Old app version
if exist app.py del app.py

REM CSV/Excel test files
if exist csv_to_rag.py del csv_to_rag.py
if exist csv_to_rag_final.py del csv_to_rag_final.py
if exist csv_to_rag_fixed.py del csv_to_rag_fixed.py
if exist direct_csv_processor.py del direct_csv_processor.py
if exist direct_csv_read.py del direct_csv_read.py
if exist direct_csv_reader.py del direct_csv_reader.py
if exist direct_excel.py del direct_excel.py
if exist direct_excel_simple.py del direct_excel_simple.py
if exist direct_excel_test.py del direct_excel_test.py
if exist excel_rag_converter.py del excel_rag_converter.py
if exist excel_reader.py del excel_reader.py
if exist excel_reader_final.py del excel_reader_final.py
if exist excel_to_rag.py del excel_to_rag.py
if exist extract_csv_data.py del extract_csv_data.py
if exist manual_csv_add.py del manual_csv_add.py
if exist manual_csv_read.py del manual_csv_read.py
if exist manual_excel_processor.py del manual_excel_processor.py
if exist process_excel_data.py del process_excel_data.py
if exist quick_csv_test.py del quick_csv_test.py
if exist read_actual_csv.py del read_actual_csv.py
if exist read_excel_data.py del read_excel_data.py
if exist read_excel_files.py del read_excel_files.py
if exist simple_csv_converter.py del simple_csv_converter.py
if exist simple_csv_reader.py del simple_csv_reader.py
if exist simple_csv_test.py del simple_csv_test.py
if exist simple_excel_read.py del simple_excel_read.py
if exist simple_extract.py del simple_extract.py

REM Old RAG versions
if exist rag_fixed_final.py del rag_fixed_final.py
if exist rag_new.py del rag_new.py
if exist rag_optimized.py del rag_optimized.py
if exist hybrid_rag.py del hybrid_rag.py
if exist manual_rag_fix.py del manual_rag_fix.py

REM Test scripts
if exist test_csv_load.py del test_csv_load.py
if exist test_csv_output.py del test_csv_output.py
if exist test_csv_simple.py del test_csv_simple.py
if exist test_multilingual.py del test_multilingual.py
if exist test_notice.py del test_notice.py
if exist test_rag_search.py del test_rag_search.py
if exist test_read.py del test_read.py
if exist quick_test.py del quick_test.py

REM Debug scripts
if exist debug_notice.py del debug_notice.py
if exist debug_rag.py del debug_rag.py
if exist check_files.py del check_files.py
if exist file_finder.py del file_finder.py
if exist fix_csv_paths.py del fix_csv_paths.py

REM Other
if exist add_new_exhibit.py del add_new_exhibit.py
if exist new_exhibit_template.txt del new_exhibit_template.txt
if exist README_complete.html del README_complete.html
if exist 0322.code-workspace del 0322.code-workspace

echo Cleanup complete!
pause
