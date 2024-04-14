import requests
from typing import Dict, Union

from config import IP_API_TOKEN


def query_ip_location(
    ip_address: str,
) -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    # IP 查询接口
    url = f"http://api.ipshudi.com/ip/?ip={ip_address}&datatype=jsonp&token={IP_API_TOKEN}"

    try:
        # 发起 GET 请求获取 IP 属地信息
        response = requests.get(url)
        data = response.json()

        # 判断是否成功获取到数据
        if data["ret"] == "ok":
            # 提取需要的信息
            country = data["data"][0]
            region = data["data"][1]
            city = data["data"][2]
            isp = data["data"][4]
            postal_code = data["data"][5]
            area_code = data["data"][6]

            # 构造字典返回结果
            result = {
                "ip": ip_address,
                "country": country,
                "region": region,
                "city": city,
                "isp": isp,
                "postal_code": postal_code,
                "area_code": area_code,
            }
            return result
        else:
            return {"error": "Failed to query IP location"}
    except Exception as e:
        raise Exception(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    ip_address = ""
    result = query_ip_location(ip_address)
    print(result)
