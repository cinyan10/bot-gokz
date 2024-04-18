def borders(content):
    lines = content.strip().split('\n')
    formatted_lines = []
    for index, line in enumerate(lines):
        if index == 0:
            formatted_lines.append(f"╔ {line}")
        elif index == len(lines) - 1:
            formatted_lines.append(f"╚ {line}")
        else:
            formatted_lines.append(f"║ {line}")
    formatted_content = '\n'.join(formatted_lines)
    return formatted_content


def server_content_borders(content):
    lines = content.strip().split('\n')
    formatted_lines = []
    for index, line in enumerate(lines):
        if index == 0:
            formatted_lines.append(f"╔═{line}")
        elif index == len(lines) - 1:
            formatted_lines.append(f"╚═{line}")
        elif line.strip().startswith('AXE'):
            formatted_lines.append(f"╠═{line}")
        else:
            formatted_lines.append(f"  {line}")
    formatted_content = '\n'.join(formatted_lines)
    return formatted_content
