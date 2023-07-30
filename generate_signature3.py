import argparse
import re

def generate_function_signature(struct_name, struct_members, postfix, comments):
    # 関数シグネチャのリスト
    function_signatures = []

    # can関数の生成
    for member_name, _ in struct_members.items():
        can_function_name = f"canSet{member_name[0].upper()}{member_name[1:]}"
        can_function_signature = f'/*! \\brief {comments.get(member_name, "")} */\n' if comments.get(member_name) else ''
        can_function_signature += f'bool {can_function_name}(const RIPBRG& key);'
        function_signatures.append(can_function_signature)

    # set関数の生成
    for member_name, member_type in struct_members.items():
        # 変数名が既にキャメルケースである場合はそのまま使用
        if not member_name[0].isupper():
            function_name = f"{member_name[0].upper()}{member_name[1:]}"
        else:
            function_name = member_name
        # 関数名の接尾にユーザー入力の文字列を追加
        function_name += postfix

        # 関数シグネチャを生成
        function_signature = f'/*! \\brief {comments.get(member_name, "")} */\n' if comments.get(member_name) else ''
        function_signature += f'int32_t set{function_name}(const RIPBRG& key, {member_type} {member_name});'
        function_signatures.append(function_signature)

    return function_signatures

def parse_cpp_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # 構造体の辞書とメンバ変数の辞書を生成
    struct_dict = {}
    comments = {}

    # 構造体の正規表現パターン
    struct_pattern = re.compile(r"struct\s+(\w+)\s*\{([^}]*)\};")

    # メンバ変数とコメントの正規表現パターン
    member_pattern = re.compile(r"/\*\!\s*\\brief\s*(.*?)\s*\*/\s*([^;]*);")

    # 構造体のマッチを検索
    for struct_match in struct_pattern.finditer(content):
        struct_name = struct_match.group(1)
        struct_members = {}
        for member_match in member_pattern.finditer(struct_match.group(2)):
            member_name = member_match.group(2).strip()
            member_type = member_match.group(1).strip()
            struct_members[member_name] = member_type
            comments[member_name] = member_match.group(1).strip()
        struct_dict[struct_name] = struct_members

    return struct_dict, comments

if __name__ == "__main__":
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(description="Generate function signatures from C++ struct")
    parser.add_argument("--cppfile", help="Path to the C++ file", required=True)
    args = parser.parse_args()

    # C++ファイルをパースして構造体情報とコメントを生成
    struct_dict, comments = parse_cpp_file(args.cppfile)

    # ユーザー入力を受け取る
    user_input = input("Enter the postfix for function names: ")

    # 各構造体に対して関数シグネチャを生成し、出力
    for struct_name, struct_members in struct_dict.items():
        function_signatures = generate_function_signature(struct_name, struct_members, user_input, comments)
        for signature in function_signatures:
            print(signature)
