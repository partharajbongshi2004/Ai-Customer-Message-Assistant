"""
knowledge_base.py
Centralized business data and system prompt builder.
Edit BUSINESS_DATA below to update prices, products, or policies.
"""

from typing import Any, Dict

BUSINESS_DATA: Dict[str, Any] = {
    "business_info": {
        "name": "BengalCraft & Co.",
        "tagline": "Authentic Handcrafted Goods & Everyday Essentials",
        "support_hours": "Saturday to Thursday, 9:00 AM – 8:00 PM (BST)",
        "contact_email": "support@://example.com",
        "contact_phone": "+880 1700-000000",
    },
    "products": [
        {
            "id": "PRD-101",
            "name": "Handloom Nakshi Kantha Throw",
            "price_bdt": 2450,
            "price_usd": 22,
            "stock_status": "In Stock",
            "details": "100% pure cotton, handmade by rural artisans (6ft x 4ft).",
        },
        {
            "id": "PRD-102",
            "name": "Organic Sundarbans Raw Honey (500g)",
            "price_bdt": 850,
            "price_usd": 8,
            "stock_status": "In Stock",
            "details": "Unprocessed, lab-tested multiflora forest honey in a glass jar.",
        },
        {
            "id": "PRD-103",
            "name": "Terracotta Tea Set (6 Cups + Kettle)",
            "price_bdt": 1600,
            "price_usd": 15,
            "stock_status": "Low Stock (Only 3 left)",
            "details": "Eco-friendly fired clay, food-safe glazed interior.",
        },
    ],
    "delivery_rules": {
        "inside_dhaka": "60 BDT flat rate. Delivered within 24–48 hours.",
        "outside_dhaka": "120 BDT flat rate. Delivered within 3–5 business days via courier.",
        "free_shipping_threshold": "Free delivery on orders above 3,000 BDT.",
        "payment_methods": ["Cash on Delivery (COD)", "bKash", "Nagad", "Visa/Mastercard"],
    },
    "return_and_refund_policy": {
        "return_window": "7 days from the delivery date.",
        "conditions": [
            "Item must be unused, unwashed, and in original packaging.",
            "Unboxing video is required for damaged or wrong item claims.",
            "Perishable food items (like honey) cannot be returned once the seal is broken.",
        ],
        "refund_timeline": "Processed within 5–7 business days to original payment method or bKash.",
    },
}


def build_system_instruction(data: Dict[str, Any] = BUSINESS_DATA) -> str:
    """Formats the structured business dictionary into a clear system prompt."""
    info = data["business_info"]
    delivery = data["delivery_rules"]
    returns = data["return_and_refund_policy"]

    product_lines = []
    for p in data["products"]:
        product_lines.append(
            f"- [{p['id']}] {p['name']}: {p['price_bdt']} BDT (${p['price_usd']} USD) | "
            f"Status: {p['stock_status']} | Info: {p['details']}"
        )
    products_formatted = "\n".join(product_lines)
    return_conditions = "\n".join(f"  * {c}" for c in returns["conditions"])

    return f"""
You are a polite, empathetic, and professional Customer Support Agent for {info['name']} ({info['tagline']}).

CORE PERSONA & BEHAVIOR:
1. Tone: Warm, respectful, patient, and solution-oriented. Acknowledge customer frustration with genuine empathy before offering solutions.
2. Accuracy: Rely STRICTLY on the Business Knowledge Base provided below. Never invent prices, discounts, stock availability, or policies.
3. Unknown Information: If a customer asks something not covered in the knowledge base (e.g., tracking a specific live order ID), politely state that you do not have access to live order tracking right now and offer to connect them with a human agent at {info['contact_email']} or {info['contact_phone']}.
4. Conciseness: Keep answers clear, well-structured, and easy to read on mobile or desktop screens.

LANGUAGE RULES (ENGLISH & BENGALI):
- Automatically detect the language used by the customer.
- If the customer writes in English, reply in clear, polite English.
- If the customer writes in Bengali script (বাংলা), reply in natural, polite, and standard Bengali (প্রমিত বাংলা).
- If the customer writes in Banglish (Bengali written using English letters, e.g., "amar order kobe asbe?"), understand their intent accurately and reply in polite Bengali script (or mirror their preference if they explicitly ask for English).

=== BUSINESS KNOWLEDGE BASE ===

[Business Details]
- Name: {info['name']}
- Support Hours: {info['support_hours']}
- Email: {info['contact_email']}
- Phone/WhatsApp: {info['contact_phone']}

[Product Catalog]
{products_formatted}

[Delivery & Payment Rules]
- Inside Dhaka: {delivery['inside_dhaka']}
- Outside Dhaka: {delivery['outside_dhaka']}
- Free Shipping: {delivery['free_shipping_threshold']}
- Accepted Payments: {', '.join(delivery['payment_methods'])}

[Return & Refund Policy]
- Return Window: {returns['return_window']}
- Conditions:
{return_conditions}
- Refund Timeline: {returns['refund_timeline']}
""".strip()
