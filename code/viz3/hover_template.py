def map_base_hover_template():
    # Generate the hover template
    return '<span style="font-family: Oswald">    %{properties.prov_name_en}</span>' + '<extra></extra>'


def map_marker_hover_template(name):
    # Generate the hover template
    return f'<span style="font-family: Oswald"> {name}</span>' + '<extra></extra>'
