import json
import google.generativeai as genai
from typing import Dict, Any, List

from RacunPlus.settings import settings


class GeminiAIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def generate(self, prompt: str) -> dict:
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json",
            },
        )

        return json.loads(response.text)

    def generate_monthly_analysis(self, bills: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not bills:
            return {
                "summary": "No bills found for this period",
                "total_amount": 0,
                "breakdown": [],
                "recommendations": ["Add bills to get analysis"]
            }

        total = sum(b['amount'] for b in bills)
        breakdown = []
        for bill in bills:
            breakdown.append({
                "provider": bill['beneficiary_name'],
                "amount": bill['amount'],
                "date": str(bill['reference_date'])
            })

        prompt = f"""
Analiziraj ove račune za ovaj mjesec i dao detaljnu analizu. 
Vrati JSON sa sljedećim poljima:
- summary: kratka analiza (tekst)
- total_amount: ukupan iznos
- breakdown: lista sa provajderima
- recommendations: lista sa preporukama (min 3)

RAČUNI:
{json.dumps(breakdown, ensure_ascii=False)}

UKUPNO: €{total:.2f}

Nastavi se kao finansijski savjetnik i dao specifične preporuke kako smanjiti troškove.
Vrati SAMO JSON, bez dodatnog teksta."""

        try:
            response_data = self.generate(prompt)
            response_data['total_amount'] = total
            return response_data
        except Exception as e:
            return {
                "summary": f"Analiza {len(bills)} računa za ovaj mjesec",
                "total_amount": total,
                "breakdown": breakdown,
                "recommendations": [
                    "Pregled vaših računa može pokazati mogućnosti za uštedu",
                    "Razmotriti bundling usluga",
                    "Provjeriti da li ste na najboljoj tarifi"
                ]
            }

    def generate_category_analysis(self, bills: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not bills:
            return {
                "summary": "No bills found for this period",
                "categories": [],
                "recommendations": ["Add bills to get analysis"]
            }

        categories_dict = {}
        total = 0
        bill_details = []
        
        for bill in bills:
            cat = bill['beneficiary_name']
            if cat not in categories_dict:
                categories_dict[cat] = []
            categories_dict[cat].append(bill['amount'])
            bill_details.append({
                "name": cat,
                "amount": bill['amount'],
                "date": str(bill['reference_date'])
            })
            total += bill['amount']

        categories_summary = []
        for cat_name, amounts in categories_dict.items():
            cat_total = sum(amounts)
            percentage = (cat_total / total * 100) if total > 0 else 0
            categories_summary.append({
                "category": cat_name,
                "total": cat_total,
                "percentage": percentage,
                "count": len(amounts)
            })

        prompt = f"""
Analiziraj ove rashode po kategorijama i dao detaljnu analizu.
Vrati JSON sa sljedećim poljima:
- summary: kratka analiza (tekst)
- categories: lista sa kategorijama, total_amount, percentage, insight
- recommendations: lista sa preporukama (min 3)

RASHODI PO KATEGORIJAMA:
{json.dumps(categories_summary, ensure_ascii=False)}

DETALJNI RASHODI:
{json.dumps(bill_details, ensure_ascii=False)}

UKUPNO: €{total:.2f}

Kao financijski analitičar, dao specifične preporuke kako smanjiti troškove po kategorijama.
Vrati SAMO JSON, bez dodatnog teksta."""

        try:
            response_data = self.generate(prompt)
            return response_data
        except Exception as e:
            categories = []
            for cat_name, amounts in categories_dict.items():
                cat_total = sum(amounts)
                percentage = (cat_total / total * 100) if total > 0 else 0
                categories.append({
                    "name": cat_name,
                    "total_amount": cat_total,
                    "percentage": round(percentage, 1),
                    "insight": f"{cat_name} je €{cat_total:.2f} ({percentage:.1f}%)"
                })

            return {
                "summary": f"Ukupno €{total:.2f} u {len(categories_dict)} kategorija",
                "categories": sorted(categories, key=lambda x: x['total_amount'], reverse=True),
                "recommendations": [
                    "Analizirati najveće rashode",
                    "Potražiti alternative za skupo usluge",
                    "Razmotriti pregovaranje sa provajderima"
                ]
            }
