import numpy as np

#=========================================================================
# Nombre         : ObjLoader
# Descripción    : Lee y organiza el archivo .obj
# Salida         : Vector orgnaizado con la información del modelo
# Source         : https://github.com/totex/Learn-OpenGL-in-python
#=========================================================================
class ObjLoader:
    buffer = []

    # =========================================================================
    # Nombre         : search_data()
    # Descripción    : Convierte los datos de string a floar o int dependiendo
    #                  de la información
    # Parámetros     : data_values - vector con los datos de la línea leída del archivo
    #                  coordinates - Vector de coordenadas para guardar el valor convertido
    #                  skip        - Caracter para diferenciar el tipo de información
    #                                'v' : Vectores de posición
    #                                'vn': Vectores normal
    #                                'f' : Caras del modelo
    #                  data_type: El tipo de dato que se deben convertir los datos
    # =========================================================================
    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d) - 1)

    # =========================================================================
    # Nombre         : create_sorted_vertex_buffer()
    # Descripción    : Convierte los datos de string a floar o int dependiendo
    #                  de la información
    # Parámetros     : indices_data - Lista de los indices tomados por la información
    #                                 dada por las líneas comenzando en 'f'
    #                  vertices     - Lista de vertices de posición
    #                  colors       - Lista de vertices de color
    #                  normals      - Lista de vertices normal
    # =========================================================================
    @staticmethod
    def create_sorted_vertex_buffer(indices_data, vertices, colors, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(vertices[start:end])
            elif i % 3 == 1:
                ObjLoader.buffer.extend(colors)
            elif i % 3 == 2:
                start = ind * 3
                end = start + 3
                ObjLoader.buffer.extend(normals[start:end])

    # =========================================================================
    # Nombre         : load_model()
    # Descripción    : Lee el modelo y llama las funciones anteriores
    # Parámetros     : file - Path del archivo
    # Salida         : Vector orgnaizado con la información del modelo
    # =========================================================================
    @staticmethod
    def load_model(file):
        vert_coords = []
        norm_coords = []
        all_indices = []
        indices = []

        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    ObjLoader.search_data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vn':
                    ObjLoader.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        val[1] = '0'
                        ObjLoader.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[2])-1)

                line = f.readline()
        col_coords = [213/255,  202/255,  212/255]
        num_max = max(vert_coords)
        if num_max > 0.72:

            for num in range(len(vert_coords)):
                vert_coords[num] = vert_coords[num] / (num_max + 100.0)
                if num % 3 == 1:
                    vert_coords[num] += -0.35
                elif num % 3 == 2:
                    vert_coords[num] -= 1.0
        ObjLoader.create_sorted_vertex_buffer(all_indices, vert_coords, col_coords, norm_coords)

        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return np.array(indices, dtype=np.uint32), buffer