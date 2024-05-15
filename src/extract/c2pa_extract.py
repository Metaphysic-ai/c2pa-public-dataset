import c2pa


class C2paExtract:
    def extract_c2pa_data(self, file_path: str):
        print (f"Extracting data from {file_path}")

        return c2pa.read_file(file_path, data_dir=None)
