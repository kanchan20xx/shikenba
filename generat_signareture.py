#coding at utf-8

# 以下はｃｐｐコードから構文解析を実施して構造体の構造体名とメンバ変数、型名、コメントを取得する処理。

import clang.cindex

# libclangを初期化
clang.cindex.Config.set_library_path("/path/to/clang/lib")  # libclangのライブラリパスを指定
index = clang.cindex.Index.create()

def extract_doxygen_comment(node):
    # Doxygenコメントを抽出
    for child in node.get_children():
        if child.kind == clang.cindex.CursorKind.INCLUSION_DIRECTIVE:
            # ヘッダーファイルのincludeディレクティブをスキップ
            continue

        comment = child.raw_comment
        if comment:
            return comment.strip()

def generate_struct_dict_with_comments(node):
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
                doxygen_comment = extract_doxygen_comment(child)

                # メンバ名とDoxygenコメントを辞書に追加
                struct_members[member_name] = {'type': member_type, 'comment': doxygen_comment}

        # 構造体情報を辞書に追加
        struct_dict[struct_name] = struct_members

    # その他のノードの場合は再帰的に子ノードをチェック
    for child in node.get_children():
        struct_dict.update(generate_struct_dict_with_comments(child))

    return struct_dict

# C++のソースファイルを解析して構造体の辞書と構造体情報を生成
def parse_cpp_file(file_path):
    translation_unit = index.parse(file_path)
    root = translation_unit.cursor

    # 構造体の辞書と構造体情報を生成
    struct_dict = generate_struct_dict_with_comments(root)
    return struct_dict

# テスト用C++ソースファイルを指定して構造体の辞書と構造体情報を生成
cpp_file_path = '/path/to/your/cpp_file.cpp'
struct_dict = parse_cpp_file(cpp_file_path)

# 構造体の辞書と構造体情報を表示
for struct_name, struct_members in struct_dict.items():
    print(f'Struct Name: {struct_name}')
    print('Members:')
    for member_name, member_info in struct_members.items():
        member_type = member_info['type']
        doxygen_comment = member_info['comment']
        print(f'  {member_name}: {member_type}')
        if doxygen_comment:
            print(f'  Comment: {doxygen_comment}')
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

# さらに改良した形　doxygenコメントをも生成できるようにした。

import re

def extract_doxygen_comment(node):
    # Doxygenコメントを抽出
    for child in node.get_children():
        if child.kind == clang.cindex.CursorKind.INCLUSION_DIRECTIVE:
            # ヘッダーファイルのincludeディレクティブをスキップ
            continue

        comment = child.raw_comment
        if comment and comment.strip().startswith("/*!"):
            return comment.strip()

def generate_function_signature(struct_name, struct_members):
    # 関数名をlower camel caseに変換
    function_name = re.sub(r'_(.)', lambda x: x.group(1).upper(), struct_name)

    # 関数シグネチャとDoxygenコメントのリスト
    function_signatures = []

    # 各メンバ変数に対して関数シグネチャとDoxygenコメントを生成
    for member_name, member_type in struct_members.items():
        # "get"を"set"に置換
        function_name_set = function_name.replace("get", "set", 1)
        function_signature = f'int32_t {function_name_set}{member_name.capitalize()}{function_name}(const RIPBRG& key, {member_type}* {member_name});'

        # Doxygenコメントを抽出
        function_comment = extract_doxygen_comment(member_name)

        if function_comment:
            # briefコメントを生成
            brief_comment = function_comment.replace("/*!", "").strip()
            # 関数コメントを基本形に合わせる
            function_signature = f'/**\n * {brief_comment}\n */\n{function_signature}'

        function_signatures.append(function_signature)

    return function_signatures

# テスト用構造体とメンバ変数の辞書
struct_name = 'Human'
struct_members = {'age': 'int', 'height': 'double', 'name': 'std::string'}

function_signatures = generate_function_signature(struct_name, struct_members)
for signature in function_signatures:
    print(signature)
