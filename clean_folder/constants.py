NEW_FOLDERS = {
    'images': [],
    'video': [],
    'audio': [],
    'documents': [],
    'archives': []
}

IGNORE_FOLDERS = {'archives', 'video', 'audio', 'documents', 'images'}

EXTENSIONS = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC', 'ICO'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV', 'GIF'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR', 'FLAC'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown': []
}

TRANSLIT = {
    1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
    1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'y', 1048: 'Y',
    1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
    1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
    1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
    1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
    1101: 'ye', 1069: 'YE', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i',
    1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'
}
