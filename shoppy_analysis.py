import requests
import pandas as pd
import matplotlib.pyplot as plt


def run():
    # shoppy url defined here for later when making get requests for order pages. 
    # required headers are useragent which can be anything and Authorization. 
    # This token can be retrieved from your shoppy developer profile
    shoppy_url = "https://shoppy.gg/api/v1/orders/"
    req_headers = {"useragent": "python", "Authorization": "key_here"}

    init = requests.get(
        shoppy_url,
        headers=req_headers)

    if init.status_code != 200:
        print(f"Status code {init.status_code}")
        return 0

    # each one of the indices in this is one page of orders, each page is 25 orders by default
    page_jsons = []
    total_pages = int(init.headers["X-Total-Pages"])

    # store all pages in json format
    for i in range(total_pages + 1):
        request_customer = requests.get(
            shoppy_url + f"?page={i + 1}",
            headers=req_headers)
        page_jsons.append(pd.read_json(request_customer.text))

    # method of getting orders per page, shoppy api does not handle this correctly and returns 25 in the headers for every page 
    # len(page_jsons[current_page]["id"])

    customer_ids = []
    customer_emails = []
    purchase_gateway = []
    purchase_amount = []

    #TODO use data structure for this
    paypal_total = 0
    stripe_total = 0
    btc_total = 0
    ltc_total = 0
    eth_total = 0

    for current_page in range(total_pages):
        for current_customer in range(len(page_jsons[current_page]["id"])):
            # only show actual confirmed purchases
            if page_jsons[current_page]["delivered"][current_customer] == 1:
                customer_ids.append(page_jsons[current_page]["id"][current_customer])
                customer_emails.append(page_jsons[current_page]["email"][current_customer])
                purchase_gateway.append(page_jsons[current_page]["gateway"][current_customer])
                purchase_amount.append(int(page_jsons[current_page]["price"][current_customer]))
                if page_jsons[current_page]["gateway"][current_customer] == "PayPal":
                    paypal_total += int(page_jsons[current_page]["price"][current_customer])
                if page_jsons[current_page]["gateway"][current_customer] == "Stripe":
                    stripe_total += int(page_jsons[current_page]["price"][current_customer])
                if page_jsons[current_page]["gateway"][current_customer] == "BTC":
                    btc_total += int(page_jsons[current_page]["price"][current_customer])
                if page_jsons[current_page]["gateway"][current_customer] == "LTC":
                    ltc_total += int(page_jsons[current_page]["price"][current_customer])
                if page_jsons[current_page]["gateway"][current_customer] == "ETH":
                    eth_total += int(page_jsons[current_page]["price"][current_customer])

    dataframe_data = {"ID": customer_ids,
                      "Email": customer_emails,
                      "Gateway": purchase_gateway,
                      "Amount": purchase_amount}
    purchase_dataframe = pd.DataFrame(dataframe_data)

    print(purchase_dataframe)

    gateway_dataframe = pd.DataFrame(
        {"$ Amount Purchased": [paypal_total, stripe_total, btc_total, ltc_total, eth_total],
         "# Times Used": [purchase_gateway.count("PayPal"),
                          purchase_gateway.count("Stripe"),
                          purchase_gateway.count("BTC"),
                          purchase_gateway.count("LTC"),
                          purchase_gateway.count("ETH")]},
        index=["Paypal", "Stripe", "BTC", "LTC", "ETH"])
    print(gateway_dataframe)

    amount_purchased_plot = gateway_dataframe.plot.pie(y="$ Amount Purchased", figsize=(5, 5))
    times_used_plot = gateway_dataframe.plot.pie(y="# Times Used", figsize=(5, 5))
    amount_purchased_plot.plot()
    times_used_plot.plot()
    plt.show()


if __name__ == "__main__":
    run()
