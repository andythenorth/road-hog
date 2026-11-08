"""Make the docs numeric ID table work with the catalogue IDs."""
from _common import ROOT, replace_once

path = ROOT / 'src/docs_templates/code_reference.pt'
replace_once(path, '<td>${consist.base_numeric_id}</td>', '<td>${doc_helper.get_base_numeric_id(consist)}</td>')
