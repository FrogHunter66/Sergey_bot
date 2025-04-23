def main(decimal_string):
    decoded_fields = list()
    decimal_number = int(decimal_string)
    fields_info = [
        ("A1", 0, 1),
        ("A2", 2, 5),
        ("A3", 6, 15),
        ("A4", 16, 18),
        ("A5", 19, 26),
        ("A6", 27, decimal_number.bit_length() - 1)
    ]

    for field_name, start_bit, end_bit in fields_info:
        field_value = (decimal_number >> start_bit) & \
                      ((1 << (end_bit - start_bit + 1)) - 1)
        decoded_fields.append((field_name, str(field_value)))
    return decoded_fields


print(main('8895923055'))