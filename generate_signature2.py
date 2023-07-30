import argparse
import clang.cindex

def get_type_spelling(t):
    # 型情報を取得する関数
    if t.kind == clang.cindex.TypeKind.POINTER:
        return get_type_spelling(t.get_pointee()) + '*'
    elif t.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
        return get_type_spelling(t.get_pointee()) + '&'
    else:
        return t.spelling

def get_doxygen_brief_comment():
    # Doxygenコメントのbrief部分を取得する関数
    return '/*!\n * \\brief\n */'

def camel_to_lower_camel(s):
    # ロウワーキャメルケースに変換する関数
    return s[0].lower() + s[1:]

def generate_function_signature(struct_name, struct_members, postfix):
    # 関数シグネチャのリスト
    function_signatures = []

    # can関数とset関数の生成
    for member_name, member_type in struct_members.items():
        # 変数名が既にキャメルケースである場合はそのまま使用
        if not member_name[0].isupper():
            function_name = f"{member_name[0].upper()}{member_name[1:]}"
        else:
            function_name = member_name
        # 関数名の接尾にユーザー入力の文字列を追加
        function_name += postfix
        function_name_lower_camel = camel_to_lower_camel(function_name)

        # 第一引数の仮引数名を生成
        first_arg_name = f"{postfix.lower()}{struct_name}Key"

        # can関数の生成
        can_function_name = f"canSet{function_name}"
        can_function_signature = f'{get_doxygen_brief_comment()}\nbool {can_function_name}(const RIPBRG_KEY &{first_arg_name});'
        function_signatures.append(can_function_signature)

        # set関数の生成
        set_function_signature = f'{get_doxygen_brief_comment()}\nint32_t set{function_name}(const RIPBRG_KEY &{first_arg_name}, {member_type} {member_name});'
        function_signatures.append(set_function_signature)

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
    parser.add_argument("--cppfile", help="Path to the C++ file", required=True)
    parser.add_argument("--libclang", help="Path to libclang library", required=True)
    args = parser.parse_args()

    # C++ファイルをパースして構造体情報を生成
    struct_dict = parse_cpp_file(args.cppfile, args.libclang)

    # ユーザー入力を受け取る
    user_input = input("Enter the postfix for function names: ")

    # 各構造体に対して関数シグネチャを生成し、出力
    for struct_name, struct_members in struct_dict.items():
        function_signatures = generate_function_signature(struct_name, struct_members, user_input)
        for signature in function_signatures:
            print(signature)
