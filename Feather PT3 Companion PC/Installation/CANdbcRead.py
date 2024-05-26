import cantools
import json

# Load the DBC file
dbc_file_path = 'VESC_CAN_PROTOCOL_experimental.dbc'
db = cantools.database.load_file(dbc_file_path)

# Initialize the dictionary to store CAN data variables
can_data_dict = {}

# Extract messages and their signals
for message in db.messages:
    signals_dict = {}
    for signal in message.signals:
        signals_dict[signal.name] = {
            'start_bit': signal.start,
            'length': signal.length,
            'byte_order': 'big_endian' if signal.byte_order == 'big_endian' else 'little_endian',
            'is_signed': signal.is_signed,
            'scale': signal.scale,
            'offset': signal.offset,
            'minimum': signal.minimum,
            'maximum': signal.maximum,
            'unit': signal.unit,
            'is_multiplexer': signal.is_multiplexer,
            'multiplexer_signal': signal.multiplexer_signal
        }
    can_data_dict[message.name] = {
        'frame_id': message.frame_id,
        'is_extended_frame': message.is_extended_frame,
        'length': message.length,
        'signals': signals_dict
    }

# Display the CAN data dictionary in a readable format
can_data_json = json.dumps(can_data_dict, indent=4)
print(can_data_json)
