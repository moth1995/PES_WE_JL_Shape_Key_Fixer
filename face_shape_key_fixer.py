from pathlib import Path
import sys
import zlib, struct
from io import BytesIO

def fix_psp_animation_face(file_path:str):
    face_file = open(file_path, "rb")
    magic_number = face_file.read(4)
    if magic_number != bytearray([0x00, 0x06, 0x01, 0x00,]):
        raise Exception("Not a valid face bin file!")
    face_file.seek(32, 0)
    face_file_unzlibbed = BytesIO(zlib.decompress(face_file.read()))
    face_file.close()
    face_file_unzlibbed.read(4 * 2)
    offset_file_1 = struct.unpack("<I", face_file_unzlibbed.read(4))[0]
    face_file_unzlibbed.seek(offset_file_1, 0)
    magic_number_3d = face_file_unzlibbed.read(4)
    if magic_number_3d != bytearray([0x03, 0x00, 0xFF, 0xFF,]):
        raise Exception("Not a PSP 3D MODEL")
    parts_info_offset = 32
    vertex_in_part_offset = 92
    shape_key_pointer = 72
    face_file_unzlibbed.seek(offset_file_1 + parts_info_offset,0)
    total_parts, part_start_offset = struct.unpack("<II", face_file_unzlibbed.read(8))
    part_start_offset += offset_file_1
    face_file_unzlibbed.seek(offset_file_1 + shape_key_pointer,0)
    shape_key_offset,_ , shape_key_end = struct.unpack("<III", face_file_unzlibbed.read(12))
    shape_key_offset += offset_file_1
    shape_key_end += offset_file_1

    i = 0
    
    new_shape_key_data = bytearray([])
    vertex_count = 0
    animations_switch_offset_list = []
    while i < total_parts and total_parts == 4:
        #print("part ",i, " offset: ", part_start_offset)
        face_file_unzlibbed.seek(part_start_offset,0)
        animations_switch_offset_list.append(part_start_offset + 20)
        part_size = struct.unpack("<I", face_file_unzlibbed.read(4))[0]

        face_file_unzlibbed.seek(4,1)
        
        vertex_start_address = struct.unpack("<I", face_file_unzlibbed.read(4))[0]
        #file.seek(part_info_start + vertex_in_part_offset,1)
        vertex_start_address += part_start_offset
        
        face_file_unzlibbed.seek(vertex_in_part_offset + part_start_offset,0)

        vertex_in_piece, vertex_size = struct.unpack("<HH", face_file_unzlibbed.read(2*2))
        face_file_unzlibbed.seek(vertex_start_address, 0)

        j = 0
        temp_vertex_data = bytearray([])
        while j < vertex_in_piece and i != 0:
            face_file_unzlibbed.read(vertex_size - 6)
            vertex_bytes = face_file_unzlibbed.read(6)
            temp_vertex_data.extend(vertex_bytes)
            j += 1
        if i == 1:
            temp_vertex_data = temp_vertex_data[-84:]
        elif i == 2:
            temp_vertex_data = temp_vertex_data[-150:]
        elif i == 3:
            temp_vertex_data = temp_vertex_data[-576:]
        
        new_shape_key_data.extend(temp_vertex_data)
        part_start_offset += part_size
        i += 1
        vertex_count += vertex_in_piece
    if vertex_count != 288:
        raise Exception("Unsupported model")
    
    face_file_unzlibbed.seek(shape_key_offset, 0)
    face_file_unzlibbed.write(new_shape_key_data)
    face_file_unzlibbed.seek(0, 2)
    new_unzlibed_size = struct.pack("<I", face_file_unzlibbed.tell())
    for i, animation_switch_offset in enumerate(animations_switch_offset_list):
        if i == 0: continue
        face_file_unzlibbed.seek(animation_switch_offset)
        face_file_unzlibbed.write(struct.pack("<I", 1))
    face_file_unzlibbed.seek(0, 0)

    new_zlibed_data = zlib.compress(face_file_unzlibbed.read(), 9)
    new_zlibed_size = struct.pack("<I", len(new_zlibed_data))
    new_face_file = open(file_path, "wb")
    new_face_file.write(bytearray([0x00, 0x06, 0x01, 0x00,]))
    new_face_file.write(new_zlibed_size)
    new_face_file.write(new_unzlibed_size)
    new_face_file.write(bytearray([0x00,] * 20))
    new_face_file.write(new_zlibed_data)
    new_face_file.close()


def fix_ps2_animation_face(file_path):
    face_file = open(file_path, "rb")
    magic_number = face_file.read(4)
    if magic_number != bytearray([0x00, 0x06, 0x01, 0x00,]):
        raise Exception("Not a valid face bin file!")
    face_file.seek(32, 0)
    face_file_unzlibbed = BytesIO(zlib.decompress(face_file.read()))
    face_file.close()
    face_file_unzlibbed.read(4 * 2)
    offset_file_1 = struct.unpack("<I", face_file_unzlibbed.read(4))[0]
    face_file_unzlibbed.seek(offset_file_1, 0)
    magic_number_3d = face_file_unzlibbed.read(4)
    if magic_number_3d != bytearray([0x03, 0x00, 0xFF, 0xFF,]):
        raise Exception("Not a PS2 3D MODEL")
    parts_info_offset = 32
    vertex_in_part_offset = 88
    shape_key_pointer = 72
    face_file_unzlibbed.seek(offset_file_1 + parts_info_offset,0)
    total_parts, part_start_offset = struct.unpack("<II", face_file_unzlibbed.read(8))
    part_start_offset += offset_file_1
    face_file_unzlibbed.seek(offset_file_1 + shape_key_pointer,0)
    shape_key_offset,_ , shape_key_end = struct.unpack("<III", face_file_unzlibbed.read(12))
    shape_key_offset += offset_file_1
    shape_key_end += offset_file_1

    i = 0
    
    new_shape_key_data = bytearray([])
    vertex_count = 0
    animations_switch_offset_list = []
    
    while i < total_parts and total_parts == 6:
        #print("part ",i, " offset: ", part_start_offset)
        face_file_unzlibbed.seek(part_start_offset,0)
        animations_switch_offset_list.append(part_start_offset + 20)

        part_size = struct.unpack("<I", face_file_unzlibbed.read(4))[0]

        face_file_unzlibbed.seek(4,1)
        
        part_info_start = struct.unpack("<I", face_file_unzlibbed.read(4))[0]-12
        
        face_file_unzlibbed.seek(part_info_start + vertex_in_part_offset,1)
        

        vertex_in_piece = struct.unpack("<H", face_file_unzlibbed.read(2))[0]

        face_file_unzlibbed.read(10)
        part_vertex_bytes = bytearray()
        if i == 1:
            part_vertex_bytes = face_file_unzlibbed.read(6 * vertex_in_piece)[-84:]
        elif i == 2:
            part_vertex_bytes = face_file_unzlibbed.read(6 * vertex_in_piece)[-150:]
        elif i == 3:
            part_vertex_bytes = face_file_unzlibbed.read(6 * vertex_in_piece)[-402:]
        elif i == 4:
            part_vertex_bytes = face_file_unzlibbed.read(6 * vertex_in_piece)[-432:]
        elif i == 5:
            part_vertex_bytes = face_file_unzlibbed.read(6 * vertex_in_piece)[-276:]

        new_shape_key_data.extend(part_vertex_bytes)
        part_start_offset += part_size
        i += 1
        vertex_count += vertex_in_piece
    if vertex_count != 372:
        raise Exception("Unsupported model")

    # if we get until this point is because the face must be supported!
    
    face_file_unzlibbed.seek(shape_key_offset, 0)
    face_file_unzlibbed.write(new_shape_key_data)
    for i, animation_switch_offset in enumerate(animations_switch_offset_list):
        if i == 0: continue
        face_file_unzlibbed.seek(animation_switch_offset)
        face_file_unzlibbed.write(struct.pack("<I", 1))

    face_file_unzlibbed.seek(0, 2)
    new_unzlibed_size = struct.pack("<I", face_file_unzlibbed.tell())
    face_file_unzlibbed.seek(0, 0)

    new_zlibed_data = zlib.compress(face_file_unzlibbed.read(), 9)
    new_zlibed_size = struct.pack("<I", len(new_zlibed_data))
    new_face_file = open(file_path, "wb")
    new_face_file.write(bytearray([0x00, 0x06, 0x01, 0x00,]))
    new_face_file.write(new_zlibed_size)
    new_face_file.write(new_unzlibed_size)
    new_face_file.write(bytearray([0x00,] * 20))
    new_face_file.write(new_zlibed_data)
    new_face_file.close()


def main():
    total_arg = len(sys.argv)
    if total_arg != 3:
        print("Invalid quantity of elements, you just need to give the path for your model")
        exit()
    
    file = Path(str(sys.argv[1]))
    version = int(sys.argv[2])
    filename = file.stem
    full_filename = file.resolve()
    
    if version == 1: # ps2
        fix_ps2_animation_face(full_filename)
        input("PS2 face file %s with animations synched" % (filename))
    elif version == 2: # psp
        fix_psp_animation_face(full_filename)
        input("PSP face file %s with animations synched" % (filename))
    else:
        raise("Unsupported version only possible values are 1 for PS2 and 2 for PSP")

if __name__ == "__main__":
    main()




