```mermaid
classDiagram
   direction LR
    class out_file_read_buffered {
        <<module>>
        int a
        
        readData(data: FileReader) DataModel
    }
    class reading_buffer_array {
        <<object>>
        int a
        
        readData(data: FileReader) DataModel
    }
    class compare_buffer_and_write_data_array {
        <<module>>
        int a
        
        readData(data: FileReader) DataModel
    }
    class buffer_parameters_array {
        <<object>>
        int a
        
        readData(data: FileReader) DataModel
    }
    class current_parameters_array {
        <<object>>
        int a
        
        readData(data: FileReader) DataModel
    }

    class IDataSaver {
        <<interface>>
        +saveData(data: ProcessedData) bool
    }
    style IDataSaver padding:0px font-family:Arial, font-size:20px, font-weight:bold fill:#f00

    class FileReader {
        +readData() DataModel
    }

    class FileWriter {
        +saveData(data: ProcessedData) bool
        
    }
    style User fill:#f9f, stroke:#333, stroke-width:2px, color:#555

    out_file_read_buffered ..|> reading_buffer_array
    reading_buffer_array ..|> compare_buffer_and_write_data_array
    compare_buffer_and_write_data_array ..|> reading_buffer_array
    compare_buffer_and_write_data_array ..|> buffer_parameters_array
    compare_buffer_and_write_data_array ..|> current_parameters_array
    buffer_parameters_array ..|> compare_buffer_and_write_data_array
    current_parameters_array ..|> compare_buffer_and_write_data_array
    FileWriter ..|> IDataSaver
    IDataProvider --> FileReader 

    class User
    class Admin
    classDef userClass fill:#f9f, stroke:#333
    classDef adminClass fill:#0f0, stroke:#f00
    class User userClass
    class Admin adminClass

