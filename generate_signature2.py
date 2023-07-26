import clang
import re

def parse_cpp_file(file_path):
    # libclangを初期化
    clang.cindex.Config.set_library_path("/usr/lib/libclang.dylib")  # libclangのライブラリパスを指定
    index = clang.cindex.Index.create()

    translation_unit = index.parse(file_path)
    root = translation_unit.cursor

    # 構造体の辞書と構造体情報を生成
    struct_dict, struct_definition = generate_struct_dict_and_struct(root)
    return struct_dict, struct_definition

def get_type_spelling(t):
    # 型情報を取得する関数
    if t.kind == clang.cindex.TypeKind.POINTER:
        return get_type_spelling(t.get_pointee()) + '*'
    elif t.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
        return get_type_spelling(t.get_pointee()) + '&'
    else:
        return t.spelling

def generate_struct_dict_and_struct(node):
    struct_dict = {}
    struct_definition = ''

    for c in node.get_children():
        if c.kind == clang.cindex.CursorKind.FIELD_DECL:
            # メンバ変数の情報を取得
            member_name = c.spelling
            member_type = get_type_spelling(c.type)
            struct_dict[member_name] = member_type

        elif c.kind == clang.cindex.CursorKind.STRUCT_DECL:
            # 構造体のネスト対応
            nested_struct_name = c.spelling
            nested_struct_dict, nested_struct_definition = generate_struct_dict_and_struct(c)
            struct_dict[nested_struct_name] = nested_struct_dict
            struct_definition += nested_struct_definition

    if node.kind == clang.cindex.CursorKind.STRUCT_DECL:
        # 構造体の定義を取得
        struct_name = node.spelling
        struct_definition += f'struct {struct_name} ' + '{\n'
        for member_name, member_type in struct_dict.items():
            if isinstance(member_type, dict):
                # ネストされた構造体の場合
                nested_struct_def = generate_struct_definition(member_name, member_type)
                struct_definition += nested_struct_def
            else:
                # メンバ変数の場合
                struct_definition += f'    {member_type} {member_name};\n'
        struct_definition += '};\n'

    return struct_dict, struct_definition

def generate_struct_definition(struct_name, struct_members):
    # 構造体の定義を生成する関数
    struct_definition = f'struct {struct_name} ' + '{\n'
    for member_name, member_type in struct_members.items():
        if isinstance(member_type, dict):
            # ネストされた構造体の場合
            nested_struct_def = generate_struct_definition(member_name, member_type)
            struct_definition += nested_struct_def
        else:
            # メンバ変数の場合
            struct_definition += f'    {member_type} {member_name};\n'
    struct_definition += '};\n'

    return struct_definition

# テスト用C++コードのパスを指定
file_path = "test_struct.cpp"

# C++ファイルをパースして構造体情報と構造体定義を生成
struct_dict, struct_definition = parse_cpp_file(file_path)

# 生成された構造体定義を表示
print(struct_definition)
