import argparse
import clang.cindex
import re

def get_type_spelling(t):
    # 型情報を取得する関数
    if t.kind == clang.cindex.TypeKind.POINTER:
        return get_type_spelling(t.get_pointee()) + '*'
    elif t.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
        return get_type_spelling(t.get_pointee()) + '&'
    else:
        return t.spelling

def generate_function_signature(struct_name, struct_members):
    # 関数名をlower camel caseに変換
    function_name = re.sub(r'_(.)', lambda x: x.group(1).upper(), struct_name)

    # 関数シグネチャのリスト
    function_signatures = []

    # 各メンバ変数に対して関数シグネチャを生成
    for member_name, member_type in struct_members.items():
        # "set"を接頭辞にし、メンバ名、構造体名の順に結合
        function_name_set = f"set{member_name.capitalize()}{function_name}"
        function_signature = f'int32_t {function_name_set}(const RIPBRG& key, {member_type}* {member_name});'
        function_signatures.append(function_signature)

    return function_signatures

def parse_cpp_file(file_path, libclang_path):
    # libclangを初期化
    clang.cindex.Config.set_library_path(libclang_path)

    index = clang.cindex.Index.create()

    translation_unit = index.parse(file_path)
    root = translation_unit.cursor

    # 構造体の辞書とメンバ変数の辞書を生成
    struct_dict = {}
    for c in root.get_children():
        if c.kind == clang.cindex.CursorKind.STRUCT_DECL and c.spelling:
            struct_name = c.spelling
            struct_members = {}
            for member in c.get_children():
                if member.kind == clang.cindex.CursorKind.FIELD_DECL:
                    member_name = member.spelling
                    member_type = get_type_spelling(member.type)
                    struct_members[member_name] = member_type
            struct_dict[struct_name] = struct_members

    return struct_dict

if __name__ == "__main__":
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description="Generate function signatures from C++ struct")
    parser.add_argument("cpp_file", help="Path to the C++ file")
    parser.add_argument("libclang_path", help="Path to libclang library")
    args = parser.parse_args()

    # C++ファイルをパースして構造体情報を生成
    struct_dict = parse_cpp_file(args.cpp_file, args.libclang_path)

    # 各構造体に対して関数シグネチャを生成し、出力
    for struct_name, struct_members in struct_dict.items():
        function_signatures = generate_function_signature(struct_name, struct_members)
        for signature in function_signatures:
            print(signature)
