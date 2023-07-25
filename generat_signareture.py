#coding at utf-8

# 以下はｃｐｐコードから構文解析を実施して構造体の構造体名とメンバ変数を取得する処理。

import clang.cindex

# libclangを初期化
clang.cindex.Config.set_library_path("/path/to/clang/lib")  # libclangのライブラリパスを指定
index = clang.cindex.Index.create()

def generate_struct_dict_and_struct(node):
    struct_dict = {}

    # ノードが構造体宣言である場合、構造体情報を辞書に追加
    if node.kind == clang.cindex.CursorKind.STRUCT_DECL:
        struct_name = node.spelling
        struct_members = {}

        # メンバ変数を辞書に追加
        for child in node.get_children():
            if child.kind == clang.cindex.CursorKind.FIELD_DECL:
                member_name = child.spelling
                member_type = child.type.spelling
                struct_members[member_name] = member_type

        # 構造体情報を辞書に追加
        struct_dict[struct_name] = struct_members

    # その他のノードの場合は再帰的に子ノードをチェック
    for child in node.get_children():
        struct_dict.update(generate_struct_dict_and_struct(child))

    return struct_dict

# C++のソースファイルを解析して構造体の辞書と構造体情報を生成
def parse_cpp_file(file_path):
    translation_unit = index.parse(file_path)
    root = translation_unit.cursor

    # 構造体の辞書と構造体情報を生成
    struct_dict = generate_struct_dict_and_struct(root)
    return struct_dict

def test_for_parse_cpp():
    # テスト用C++ソースファイルを指定して構造体の辞書と構造体情報を生成
    cpp_file_path = '/path/to/your/cpp_file.cpp'
    struct_dict = parse_cpp_file(cpp_file_path)

    # 構造体の辞書と構造体情報を表示
    for struct_name, struct_members in struct_dict.items():
        print(f'Struct Name: {struct_name}')
        print('Members:')
        for member_name, member_type in struct_members.items():
            print(f'  {member_name}: {member_type}')
        print('\n')

# ここからは辞書と構造名からシグネチャを作る処理
import re

def generate_function_signature(struct_name, struct_members):
    # 関数名をlower camel caseに変換
    function_name = re.sub(r'_(.)', lambda x: x.group(1).upper(), struct_name)

    # 関数シグネチャのリスト
    function_signatures = []

    # 各メンバ変数に対して関数シグネチャを生成
    for member_name, member_type in struct_members.items():
        function_signature = f'int32_t get{member_name.capitalize()}{function_name}(const RIPBRG& key, {member_type}* {member_name}) {{\n    // 関数の実装をここに記述\n}}\n'
        function_signatures.append(function_signature)

    return function_signatures

# テスト用構造体とメンバ変数の辞書
struct_name = 'Human'
struct_members = {'age': 'int', 'height': 'double', 'name': 'std::string'}

function_signatures = generate_function_signature(struct_name, struct_members)

# 関数シグネチャをcppファイルに出力
output_file_path = '/path/to/your/cpp_file.cpp'
with open(output_file_path, 'w') as output_file:
    for signature in function_signatures:
        output_file.write(signature)
