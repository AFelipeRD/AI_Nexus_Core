#!/usr/bin/env python3
"""
Job Search Automation — AI_Nexus_Core
Automatiza búsqueda multi-plataforma, adaptación de CV, cartas de presentación y tracking de aplicaciones.

Perfil: Andres Felipe Rincon Duarte
- Data Engineer | Data Analytics | Applied AI Engineer
- Bogotá D.C., Colombia | Remoto / Híbrido
- Salario objetivo: ≥ 3.600.000 COP/mes
- Empresas grandes, career growth
- Inglés básico
- Stack: GCP/BigQuery, Python, SQL, SAS, Ollama, vLLM, MCP, Agentic Workflows, RAG, Scikit-Learn, XGBoost, Power BI, Looker
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, quote_plus

import aiohttp
from bs4 import BeautifulSoup

# ============================
# CONFIGURACIÓN DEL PERFIL
# ============================

@dataclass
class Profile:
    nombre: str = "Andres Felipe Rincon Duarte"
    titulo: str = "Data Engineer | Data Analytics | Applied AI Engineer"
    ubicacion: str = "Bogotá D.C., Colombia"
    telefono: str = "(+57) 320 5307698"
    email: str = "afrsenju@outlook.com"
    linkedin: str = "https://linkedin.com/in/afeliperincond"
    github: str = "https://github.com/AFelipeRD"
    salario_min_cop: int = 3_600_000
    modalidad: list[str] = field(default_factory=lambda: ["Remoto", "Híbrido"])
    idiomas: dict[str, str] = field(default_factory=lambda: {"Español": "Nativo", "Inglés": "Básico (A2-B1)"})
    disponibilidad: str = "Inmediata"
    
    # Hard skills (del CV)
    cloud_data: list[str] = field(default_factory=lambda: [
        "GCP", "BigQuery", "Cloud Storage", "ETL/ELT", "APIs REST/OAuth2",
        "Data Quality", "Modelado Dimensional", "Cloud Storage"
    ])
    ia_ml: list[str] = field(default_factory=lambda: [
        "Ollama", "vLLM", "Laya", "MCP", "Agentic Workflows", "RAG",
        "Scikit-Learn", "XGBoost", "NLP", "LLMs locales", "Llama 3", "Mistral"
    ])
    lenguajes_bd: list[str] = field(default_factory=lambda: [
        "Python (Pandas, Polars, FastAPI)", "JSON", "SQL Avanzado",
        "MySQL", "SQL Server", "SAS"
    ])
    bi: list[str] = field(default_factory=lambda: [
        "Power BI (DAX, Power Query, HTML/CSS)", "Looker", "Excel Avanzado"
    ])
    herramientas: list[str] = field(default_factory=lambda: ["Git", "Scrum", "GitHub Actions"])
    
    # Experiencia clave (bullets para cartas)
    logros: list[str] = field(default_factory=lambda: [
        "Reducí 95 % tiempos de procesamiento ETL/ELT en GCP/BigQuery (sector financiero)",
        "Habilité información Qualtrics tras 3 años sin acceso via APIs + Python",
        "Dashboards Power BI/Looker para 250+ stakeholders con actualización diaria",
        "Automatización informes SMTP/OAuth2: -15h/semana trabajo manual",
        "Data Quality validations + runbooks reproducibles",
        "Despliegue LLMs locales (Ollama/vLLM) para privacidad de datos",
        "Servidores MCP conectando LLMs con BDs y APIs + flujos agénticos",
        "Entrenamiento ML clásico (Scikit-Learn, XGBoost) + análisis sentimiento con Laya",
        "Arquitectura modular, commits semánticos, CI/CD con GitHub Actions"
    ])
    
    # Cargos objetivo
    target_roles: list[str] = field(default_factory=lambda: [
        "Data Engineer", "Data Analytics Engineer", "Applied AI Engineer",
        "ML Engineer", "Data Scientist", "Analytics Engineer",
        "Big Data Engineer", "ETL Developer", "Business Intelligence Engineer"
    ])
    
    # Keywords para búsqueda
    search_keywords: list[str] = field(default_factory=lambda: [
        "Data Engineer", "Data Analytics", "Applied AI", "Machine Learning",
        "GCP", "BigQuery", "Python", "SQL", "ETL", "ELT",
        "Power BI", "Looker", "Ollama", "MCP", "Agentic", "RAG",
        "Scikit-Learn", "XGBoost", "NLP", "LLM", "vLLM"
    ])
    
    # Empresas objetivo (grandes en Colombia / remoto LatAm)
    target_companies: list[str] = field(default_factory=lambda: [
        # Bancos / Fintech
        "Bancolombia", "Daviplata", "Nequi", "RappiPay", "Movii",
        # Tech / Startups escala
        "Rappi", "MercadoLibre", "Globant", "Endava", "PSL",
        "Encora", "Nearsoft", "Belatrix", "Arkus", "Koombea",
        # Enterprise / Consultoría
        "Accenture", "Deloitte", "EY", "KPMG", "PwC",
        "IBM", "Microsoft", "Google", "AWS", "Oracle",
        # Salud / Seguros
        "Sura", "Colsanitas", "Seguros Bolívar", "Allianz",
        # Retail / Consumo
        "Éxito", "Falabella", "Cencosud", "Alkosto",
        # Telecom
        "Claro", "Tigo", "Movistar", "ETB",
        # Gobierno / Sector público
        "MinTIC", "DANE", "Banco de la República"
    ])


PROFILE = Profile()

# ============================
# ESTRUCTURAS DE DATOS
# ============================

@dataclass
class JobPosting:
    id: str
    titulo: str
    empresa: str
    ubicacion: str
    modalidad: str
    salario: Optional[str]
    descripcion: str
    requisitos: list[str]
    url: str
    plataforma: str
    fecha_publicacion: Optional[str] = None
    fecha_scrape: str = field(default_factory=lambda: datetime.now().isoformat())
    match_score: float = 0.0
    cv_adaptado: bool = False
    carta_generada: bool = False
    aplicado: bool = False
    fecha_aplicacion: Optional[str] = None
    notas: str = ""

@dataclass
class Application:
    job_id: str
    fecha: str
    cv_path: str
    carta_path: str
    plataforma: str
    estado: str = "Enviado"  # Enviado, En revisión, Entrevista, Oferta, Rechazado
    seguimiento: list[str] = field(default_factory=list)


# ============================
# SCRAPERS MULTI-PLATAFORMA
# ============================

class JobScraper:
    """Base scraper con rate-limiting y headers realistas."""
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    def __init__(self, rate_limit: float = 2.0):
        self.rate_limit = rate_limit
        self.last_request = 0.0
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=5)
        self.session = aiohttp.ClientSession(headers=self.HEADERS, timeout=timeout, connector=connector)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _get(self, url: str) -> str:
        now = time.time()
        wait = self.rate_limit - (now - self.last_request)
        if wait > 0:
            await asyncio.sleep(wait)
        self.last_request = time.time()
        
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            return await resp.text()
    
    def _parse_salary(self, text: str) -> Optional[str]:
        """Extrae salario del texto (COP, USD, rangos)."""
        patterns = [
            r'[\$€£]\s*[\d.,]+\s*[KM]?',  # $3,600,000 o $3.6M
            r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s*(?:COP|USD|EUR)',
            r'(?:salario|sueldo|rango)\s*(?:de\s*)?[\d.,]+\s*[KM]?',
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(0).strip()
        return None
    
    def _calculate_match(self, job: JobPosting) -> float:
        """Calcula score de coincidencia 0-1 basado en keywords del perfil."""
        text = f"{job.titulo} {job.descripcion} {' '.join(job.requisitos)}".lower()
        matches = sum(1 for kw in PROFILE.search_keywords if kw.lower() in text)
        return min(1.0, matches / max(1, len(PROFILE.search_keywords) * 0.3))


class ComputrabajoScraper(JobScraper):
    """Scraper para Computrabajo Colombia."""
    
    BASE_URL = "https://co.computrabajo.com"
    
    async def search(self, keywords: list[str], location: str = "bogota", pages: int = 3) -> list[JobPosting]:
        jobs = []
        for kw in keywords[:5]:  # Limitar para rate-limit
            query = quote_plus(kw)
            for page in range(1, pages + 1):
                url = f"{self.BASE_URL}/empleos-en-{location}?q={query}&p={page}"
                try:
                    html = await self._get(url)
                    jobs.extend(self._parse_listing(html, kw))
                except Exception as e:
                    print(f"[Computrabajo] Error en {url}: {e}")
        return jobs
    
    def _parse_listing(self, html: str, keyword: str) -> list[JobPosting]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        for article in soup.select("article.box_offer, .job_item, [data-job-id]"):
            try:
                # Título y URL
                title_elem = article.select_one("h2 a, h1 a, .job-title a, a.js_o_link")
                if not title_elem:
                    continue
                titulo = title_elem.get_text(strip=True)
                url = title_elem.get("href", "")
                if url and not url.startswith("http"):
                    url = self.BASE_URL + url
                
                # Empresa
                empresa_elem = article.select_one(".company-name, .fc_base, [data-company]")
                empresa = empresa_elem.get_text(strip=True) if empresa_elem else "No especificada"
                
                # Ubicación
                loc_elem = article.select_one(".location, .fs13, [data-location]")
                ubicacion = loc_elem.get_text(strip=True) if loc_elem else "Colombia"
                
                # Salario
                salario_elem = article.select_one(".salary, .fs16, [data-salary]")
                salario = salario_elem.get_text(strip=True) if salario_elem else None
                
                # Descripción breve
                desc_elem = article.select_one(".description, .job-description, p")
                descripcion = desc_elem.get_text(strip=True)[:500] if desc_elem else ""
                
                # ID único
                job_id = f"computrabajo_{hash(url) % 1000000}"
                
                job = JobPosting(
                    id=job_id,
                    titulo=titulo,
                    empresa=empresa,
                    ubicacion=ubicacion,
                    modalidad="No especificada",
                    salario=salario,
                    descripcion=descripcion,
                    requisitos=[],
                    url=url,
                    plataforma="Computrabajo",
                )
                job.match_score = self._calculate_match(job)
                
                # Filtrar por salario mínimo si está disponible
                if job.match_score > 0.15:  # Threshold mínimo
                    jobs.append(job)
                    
            except Exception as e:
                continue
        return jobs


class ElempleoScraper(JobScraper):
    """Scraper para Elempleo.com Colombia."""
    
    BASE_URL = "https://www.elempleo.com"
    
    async def search(self, keywords: list[str], pages: int = 3) -> list[JobPosting]:
        jobs = []
        for kw in keywords[:5]:
            query = quote_plus(kw)
            for page in range(1, pages + 1):
                url = f"{self.BASE_URL}/co/empleos?keyword={query}&page={page}"
                try:
                    html = await self._get(url)
                    jobs.extend(self._parse_listing(html, kw))
                except Exception as e:
                    print(f"[Elempleo] Error en {url}: {e}")
        return jobs
    
    def _parse_listing(self, html: str, keyword: str) -> list[JobPosting]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        for card in soup.select(".job-card, .vacancy-item, article.job"):
            try:
                titulo_elem = card.select_one("h2 a, h3 a, .job-title a")
                if not titulo_elem:
                    continue
                titulo = titulo_elem.get_text(strip=True)
                url = titulo_elem.get("href", "")
                if url and not url.startswith("http"):
                    url = self.BASE_URL + url
                
                empresa_elem = card.select_one(".company, .employer-name")
                empresa = empresa_elem.get_text(strip=True) if empresa_elem else "No especificada"
                
                ubicacion_elem = card.select_one(".location, .city")
                ubicacion = ubicacion_elem.get_text(strip=True) if ubicacion_elem else "Colombia"
                
                salario_elem = card.select_one(".salary, .remuneration")
                salario = salario_elem.get_text(strip=True) if salario_elem else None
                
                desc_elem = card.select_one(".description, .summary")
                descripcion = desc_elem.get_text(strip=True)[:500] if desc_elem else ""
                
                job_id = f"elempleo_{hash(url) % 1000000}"
                
                job = JobPosting(
                    id=job_id,
                    titulo=titulo,
                    empresa=empresa,
                    ubicacion=ubicacion,
                    modalidad="No especificada",
                    salario=salario,
                    descripcion=descripcion,
                    requisitos=[],
                    url=url,
                    plataforma="Elempleo",
                )
                job.match_score = self._calculate_match(job)
                
                if job.match_score > 0.15:
                    jobs.append(job)
            except Exception:
                continue
        return jobs


class IndeedScraper(JobScraper):
    """Scraper para Indeed Colombia."""
    
    BASE_URL = "https://co.indeed.com"
    
    async def search(self, keywords: list[str], location: str = "Bogotá", pages: int = 3) -> list[JobPosting]:
        jobs = []
        for kw in keywords[:5]:
            query = quote_plus(kw)
            loc = quote_plus(location)
            for page in range(0, pages * 10, 10):
                url = f"{self.BASE_URL}/jobs?q={query}&l={loc}&start={page}"
                try:
                    html = await self._get(url)
                    jobs.extend(self._parse_listing(html, kw))
                except Exception as e:
                    print(f"[Indeed] Error en {url}: {e}")
        return jobs
    
    def _parse_listing(self, html: str, keyword: str) -> list[JobPosting]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        for card in soup.select(".job_seen_beacon, .result, .job_card"):
            try:
                titulo_elem = card.select_one("h2 a, .jobTitle a, [data-jk]")
                if not titulo_elem:
                    continue
                titulo = titulo_elem.get_text(strip=True)
                url = titulo_elem.get("href", "")
                if url and not url.startswith("http"):
                    url = self.BASE_URL + url
                
                empresa_elem = card.select_one(".companyName, [data-testid='company-name']")
                empresa = empresa_elem.get_text(strip=True) if empresa_elem else "No especificada"
                
                ubicacion_elem = card.select_one(".companyLocation, [data-testid='job-location']")
                ubicacion = ubicacion_elem.get_text(strip=True) if ubicacion_elem else "Colombia"
                
                salario_elem = card.select_one(".salary-snippet, .salary")
                salario = salario_elem.get_text(strip=True) if salario_elem else None
                
                desc_elem = card.select_one(".job-snippet, .summary")
                descripcion = desc_elem.get_text(strip=True)[:500] if desc_elem else ""
                
                job_id = f"indeed_{hash(url) % 1000000}"
                
                job = JobPosting(
                    id=job_id,
                    titulo=titulo,
                    empresa=empresa,
                    ubicacion=ubicacion,
                    modalidad="No especificada",
                    salario=salario,
                    descripcion=descripcion,
                    requisitos=[],
                    url=url,
                    plataforma="Indeed",
                )
                job.match_score = self._calculate_match(job)
                
                if job.match_score > 0.15:
                    jobs.append(job)
            except Exception:
                continue
        return jobs


class GoogleJobsScraper(JobScraper):
    """Scraper para Google Jobs (via search HTML)."""
    
    BASE_URL = "https://www.google.com"
    
    async def search(self, keywords: list[str], pages: int = 2) -> list[JobPosting]:
        jobs = []
        for kw in keywords[:5]:
            query = quote_plus(f"{kw} empleo Colombia remoto")
            for page in range(pages):
                start = page * 10
                url = f"{self.BASE_URL}/search?q={query}&start={start}&hl=es"
                try:
                    html = await self._get(url)
                    jobs.extend(self._parse_listing(html, kw))
                except Exception as e:
                    print(f"[Google] Error en {url}: {e}")
        return jobs
    
    def _parse_listing(self, html: str, keyword: str) -> list[JobPosting]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        # Google Jobs aparece en contenedores específicos
        for card in soup.select(".g, .VwiC3b, .ULSxyf"):
            try:
                # Buscar enlaces que parezcan ofertas de empleo
                links = card.select("a[href*='empleo'], a[href*='job'], a[href*='vacante'], a[href*='trabajo']")
                for link in links:
                    titulo = link.get_text(strip=True)
                    url = link.get("href", "")
                    if not titulo or len(titulo) < 10:
                        continue
                    if not url.startswith("http"):
                        continue
                    
                    # Filtrar dominios de empleo conocidos
                    job_domains = ["computrabajo", "elempleo", "indeed", "linkedin", "glassdoor", "ziprecruiter", "talent", "bumeran", "zonajobs"]
                    if not any(d in url for d in job_domains):
                        continue
                    
                    job_id = f"google_{hash(url) % 1000000}"
                    
                    job = JobPosting(
                        id=job_id,
                        titulo=titulo[:200],
                        empresa="Por identificar",
                        ubicacion="Colombia",
                        modalidad="No especificada",
                        salario=None,
                        descripcion="",
                        requisitos=[],
                        url=url,
                        plataforma="Google Jobs",
                    )
                    job.match_score = self._calculate_match(job)
                    
                    if job.match_score > 0.1:
                        jobs.append(job)
            except Exception:
                continue
        return jobs


class LinkedInScraper(JobScraper):
    """Scraper básico para LinkedIn (requiere login para resultados completos).
    Usa búsqueda pública limitada."""
    
    BASE_URL = "https://www.linkedin.com"
    
    async def search(self, keywords: list[str], pages: int = 2) -> list[JobPosting]:
        # LinkedIn requiere login para resultados reales
        # Esta versión usa búsqueda pública limitada
        jobs = []
        for kw in keywords[:3]:
            query = quote_plus(f"{kw} Colombia site:linkedin.com/jobs")
            url = f"https://www.google.com/search?q={query}"
            try:
                html = await self._get(url)
                jobs.extend(self._parse_listing(html, kw))
            except Exception as e:
                print(f"[LinkedIn] Error: {e}")
        return jobs
    
    def _parse_listing(self, html: str, keyword: str) -> list[JobPosting]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        
        for link in soup.select("a[href*='linkedin.com/jobs']"):
            try:
                titulo = link.get_text(strip=True)
                url = link.get("href", "")
                if not titulo or len(titulo) < 10:
                    continue
                
                job_id = f"linkedin_{hash(url) % 1000000}"
                
                job = JobPosting(
                    id=job_id,
                    titulo=titulo[:200],
                    empresa="LinkedIn",
                    ubicacion="Colombia",
                    modalidad="No especificada",
                    salario=None,
                    descripcion="",
                    requisitos=[],
                    url=url,
                    plataforma="LinkedIn",
                )
                job.match_score = self._calculate_match(job)
                
                if job.match_score > 0.1:
                    jobs.append(job)
            except Exception:
                continue
        return jobs


# ============================
# GENERADOR DE CV Y CARTA
# ============================

class DocumentGenerator:
    """Genera CV y carta adaptados para cada vacante."""
    
    def __init__(self, profile: Profile):
        self.profile = profile
    
    def _select_relevant_skills(self, job: JobPosting) -> dict[str, list[str]]:
        """Selecciona skills relevantes basándose en la descripción del puesto."""
        text = f"{job.titulo} {job.descripcion} {' '.join(job.requisitos)}".lower()
        
        relevant = {}
        all_skills = {
            "Cloud y Data Eng": self.profile.cloud_data,
            "IA y ML": self.profile.ia_ml,
            "Lenguajes y BD": self.profile.lenguajes_bd,
            "BI": self.profile.bi,
            "Herramientas": self.profile.herramientas,
        }
        
        for category, skills in all_skills.items():
            relevant[category] = [s for s in skills if any(kw in text for kw in s.lower().split())]
            if not relevant[category]:
                # Incluir top 3 de cada categoría como fallback
                relevant[category] = skills[:3]
        
        return relevant
    
    def _select_relevant_logros(self, job: JobPosting) -> list[str]:
        """Selecciona logros más relevantes para el puesto."""
        text = f"{job.titulo} {job.descripcion}".lower()
        
        # Keywords que mapean a logros específicos
        mapping = {
            "etl": 0, "elt": 0, "pipeline": 0, "bigquery": 0, "gcp": 0,
            "qualtrics": 1, "api": 1, "api rest": 1,
            "dashboard": 2, "power bi": 2, "looker": 2, "stakeholder": 2,
            "automatiz": 3, "smtp": 3, "oauth": 3, "informe": 3,
            "data quality": 4, "validac": 4, "runbook": 4,
            "ollama": 5, "vllm": 5, "llm": 5, "mcp": 5, "agentic": 5, "rag": 5,
            "scikit": 6, "xgboost": 6, "machine learning": 6, "ml": 6, "sentimiento": 6,
            "git": 7, "github actions": 7, "ci/cd": 7, "arquitectura": 7,
        }
        
        scores = {i: 0 for i in range(len(self.profile.logros))}
        for kw, idx in mapping.items():
            if kw in text.lower():
                scores[idx] += 1
        
        # Ordenar por score y tomar top 4
        sorted_logros = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self.profile.logros[i] for i, _ in sorted_logros[:4] if _ > 0] or self.profile.logros[:4]
    
    def generate_cv_html(self, job: JobPosting) -> str:
        """Genera CV HTML adaptado."""
        relevant_skills = self._select_relevant_skills(job)
        relevant_logros = self._select_relevant_logros(job)
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{self.profile.nombre} - {job.titulo}</title>
<style>
@page {{ size: letter; margin: 12mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 8.8pt; line-height: 1.34; color: #1E293B; margin: 0; padding: 0; }}
.page {{ max-width: 186mm; margin: 0 auto; }}
header {{ text-align: center; padding: 0 0 7px; margin-bottom: 9px; border-bottom: 2.5px solid #1E3A8A; }}
h1 {{ font-size: 22pt; line-height: 1.05; letter-spacing: 2px; margin: 0 0 3px; color: #0F172A; font-weight: 800; }}
.headline {{ font-size: 10pt; color: #1E3A8A; font-weight: 600; margin: 0 0 4px; letter-spacing: .3px; }}
.contact {{ font-size: 8.5pt; color: #64748B; margin: 0; }}
.contact .sep {{ color: #CBD5E1; margin: 0 5px; }}
a {{ color: #1E293B; text-decoration: none; border-bottom: 1px solid #CBD5E1; }}
section {{ margin-bottom: 8px; }}
h2 {{ font-size: 9.4pt; text-transform: uppercase; letter-spacing: 1.4px; color: #0F172A; font-weight: 700; margin: 0 0 4px; padding: 0 0 2px 7px; border-left: 3px solid #1E3A8A; border-bottom: 1px solid #E2E8F0; }}
h3 {{ font-size: 9.2pt; margin: 4px 0 2px; color: #0F172A; font-weight: 700; }}
.org {{ color: #1E3A8A; }}
.dates {{ float: right; color: #64748B; font-weight: 500; font-size: 8.5pt; }}
.entry {{ page-break-inside: avoid; }}
ul {{ margin: 0 0 2px; padding-left: 14px; }}
li {{ margin-bottom: 1.5px; }}
li::marker {{ color: #1E3A8A; }}
strong {{ font-weight: 600; color: #0F172A; }}
.skills p {{ margin-bottom: 1.5px; }}
.target-job {{ background: #F0F4FF; border-left: 3px solid #1E3A8A; padding: 6px 10px; margin-bottom: 8px; font-size: 8.5pt; }}
</style>
</head>
<body>
<div class="page">
<header>
  <h1>{self.profile.nombre.upper()}</h1>
  <p class="headline">{job.titulo} | {self.profile.titulo}</p>
  <p class="contact">
    {self.profile.ubicacion}<span class="sep">|</span>{self.profile.telefono}<span class="sep">|</span><a href="mailto:{self.profile.email}">{self.profile.email}</a><span class="sep">|</span><a href="{self.profile.linkedin}">{self.profile.linkedin}</a><span class="sep">|</span><a href="{self.profile.github}">{self.profile.github}</a>
  </p>
</header>

<div class="target-job">
  <strong>Postulación a:</strong> {job.titulo} en {job.empresa} ({job.ubicacion}, {job.modalidad})
</div>

<section>
  <h2>Professional Summary</h2>
  <p>Ingeniero de Sistemas titulado y Data Engineer con experiencia en sector financiero, diseñando pipelines ETL/ELT sobre GCP/BigQuery con Python, SQL y SAS. Reduje en un 95% los tiempos de procesamiento y entregué soluciones analíticas para 250+ stakeholders. Desarrollo independiente de IA aplicada: modelos locales (Ollama, vLLM), servidores MCP y flujos agénticos.</p>
</section>

<section>
  <h2>Professional Experience</h2>
  <div class="entry">
    <h3>Data Engineer / Data Analytics — <span class="org">Banco de Bogotá (Summar)</span><span class="dates">07/2025 – 06/2026</span></h3>
    <ul>
"""
        for logro in relevant_logros:
            html += f"      <li>{logro}</li>\n"
        
        html += """    </ul>
  </div>
  <div class="entry">
    <h3>Especialista Soporte IT — <span class="org">Atento Colombia (Kibernum)</span><span class="dates">06/2024 – 02/2025</span></h3>
    <ul>
      <li>300+ incidencias resueltas (Nivel 1/2), 92% SLA, -20% inactividad operativa.</li>
    </ul>
  </div>
  <div class="entry">
    <h3>Independent Projects<span class="dates">01/2026 – Presente</span></h3>
    <ul>
"""
        for logro in self.profile.logros[6:]:  # Proyectos independientes
            html += f"      <li>{logro}</li>\n"
        
        html += """    </ul>
  </div>
</section>

<section class="skills entry">
  <h2>Technical Skills</h2>
"""
        for category, skills in relevant_skills.items():
            html += f"  <p><strong>{category}:</strong> {', '.join(skills)}</p>\n"
        
        html += f"""</section>

<section class="entry">
  <h2>Education</h2>
  <h3>Ingeniería de Sistemas / B.Sc. — <span class="org">UNIMINUTO</span><span class="dates">01/2020 – 04/2026</span></h3>
  <p>Titulado. Énfasis: Arquitecturas Cloud (GCP), Ingeniería de Datos, Pipelines ETL/ELT y Analítica Avanzada.</p>
</section>

<section class="entry">
  <h2>Certifications</h2>
  <p><strong>ItCertificate.us (05/2025):</strong></p>
  <ul>
    <li>Data Scientist Certified Specialist (DSCS), Big Data Certified Professional (BDCP), Data Analytics Certified Professional (DACP), Big Data Certified Associate (BDCA).</li>
  </ul>
  <p><strong>Otros:</strong> Microsoft Office Specialist Excel Associate (Certiport) · Big Data, Data Science y Analytics 480h (EXACOM I.T., 2025) · ETL Modernos con Python y Git (CódigoFacilito).</p>
</section>
</div>
</body>
</html>"""
        return html
    
    def generate_cover_letter_html(self, job: JobPosting) -> str:
        """Genera carta de presentación adaptada."""
        relevant_logros = self._select_relevant_logros(job)
        
        # Extraer requisitos clave de la descripción
        req_keywords = []
        text = f"{job.titulo} {job.descripcion}".lower()
        for kw in self.profile.search_keywords:
            if kw.lower() in text:
                req_keywords.append(kw)
        
        req1 = req_keywords[0] if len(req_keywords) > 0 else "ingeniería de datos robusta"
        req2 = req_keywords[1] if len(req_keywords) > 1 else "soluciones analíticas escalables"
        req3 = req_keywords[2] if len(req_keywords) > 2 else "gobernanza del dato"
        
        logro1 = relevant_logros[0] if relevant_logros else self.profile.logros[0]
        logro2 = relevant_logros[1] if len(relevant_logros) > 1 else self.profile.logros[1]
        
        fecha = datetime.now().strftime("%d de %B de %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Carta de Presentación - {self.profile.nombre}</title>
<style>
@page {{ size: letter; margin: 16mm 18mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 10pt; line-height: 1.55; color: #1E293B; margin: 0; padding: 0; }}
.page {{ max-width: 180mm; margin: 0 auto; }}
header {{ text-align: center; padding: 0 0 8px; margin-bottom: 18px; border-bottom: 2.5px solid #1E3A8A; }}
h1 {{ font-size: 22pt; line-height: 1.05; letter-spacing: 2px; margin: 0 0 4px; color: #0F172A; font-weight: 800; }}
.headline {{ font-size: 10pt; color: #1E3A8A; font-weight: 600; margin: 0 0 5px; letter-spacing: .3px; }}
.contact {{ font-size: 8.5pt; color: #64748B; margin: 0; }}
.contact .sep {{ color: #CBD5E1; margin: 0 5px; }}
a {{ color: #1E293B; text-decoration: none; border-bottom: 1px solid #CBD5E1; }}
.meta {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }}
.recipient p {{ margin: 0; line-height: 1.5; }}
.recipient .name {{ font-weight: 700; color: #0F172A; }}
.recipient .detail {{ color: #64748B; }}
.date {{ color: #64748B; font-weight: 500; font-size: 9pt; white-space: nowrap; }}
.subject {{ font-size: 10pt; font-weight: 700; color: #0F172A; margin: 0 0 14px; padding: 0 0 3px 8px; border-left: 3px solid #1E3A8A; border-bottom: 1px solid #E2E8F0; }}
p {{ margin: 0 0 11px; text-align: left; }}
.greeting {{ margin-bottom: 11px; }}
strong {{ font-weight: 600; color: #0F172A; }}
.closing {{ margin-top: 16px; }}
.closing p {{ margin-bottom: 3px; }}
.signature {{ margin-top: 18px; padding-top: 8px; border-top: 1px solid #E2E8F0; }}
.signature .name {{ font-size: 12pt; font-weight: 800; letter-spacing: 1px; color: #0F172A; margin: 0 0 1px; }}
.signature .role {{ font-size: 9pt; color: #1E3A8A; font-weight: 600; margin: 0 0 3px; }}
.signature .links {{ font-size: 8.5pt; color: #64748B; margin: 0; }}
.signature .sep {{ color: #CBD5E1; margin: 0 5px; }}
</style>
</head>
<body>
<div class="page">
<header>
  <h1>{self.profile.nombre.upper()}</h1>
  <p class="headline">{self.profile.titulo}</p>
  <p class="contact">
    {self.profile.ubicacion}<span class="sep">|</span>{self.profile.telefono}<span class="sep">|</span><a href="mailto:{self.profile.email}">{self.profile.email}</a><span class="sep">|</span><a href="{self.profile.linkedin}">{self.profile.linkedin}</a><span class="sep">|</span><a href="{self.profile.github}">{self.profile.github}</a>
  </p>
</header>

<div class="meta">
  <div class="recipient">
    <p class="name">Equipo de Talento / [Nombre del Reclutador]</p>
    <p class="detail">{job.empresa}</p>
    <p class="detail">{job.ubicacion} / {job.modalidad}</p>
  </div>
  <div class="date">{fecha}</div>
</div>

<p class="subject">Asunto: Postulación a {job.titulo} - {self.profile.nombre}</p>

<p class="greeting">Estimado equipo de {job.empresa}:</p>

<p>Un <strong>{job.titulo}</strong> eficaz necesita dos cosas que rara vez llegan en una misma persona: la ingeniería de datos que sostiene al negocio y la IA aplicada que lo acelera. Escribo porque mi perfil combina ambas, y porque su necesidad de <strong>{req1}</strong> y <strong>{req2}</strong> coincide con lo que he construido.</p>

<p><strong>Ingeniería de datos con impacto de negocio.</strong> En el sector financiero diseñé pipelines ETL/ELT sobre GCP/BigQuery con Python, SQL y SAS que redujeron en un <strong>95 %</strong> los tiempos de procesamiento, y habilité por primera vez en más de 3 años la información de encuestas Qualtrics mediante APIs seguras. Implementé validaciones de Data Quality y runbooks que garantizan reproducibilidad y gobierno del dato, y entregué dashboards en Power BI y Looker a más de <strong>250 stakeholders</strong>. Esa experiencia se traduce directamente en <strong>{req3}</strong> para su equipo.</p>

<p><strong>Mi diferenciador: IA aplicada.</strong> De forma independiente, desde enero de 2026, construyo soluciones de IA: despliego modelos locales con <strong>Ollama y vLLM</strong> para proteger la privacidad de los datos, diseño servidores <strong>MCP (Model Context Protocol)</strong> que conectan LLMs con bases de datos y APIs, desarrollo flujos agénticos y entreno modelos de ML clásico con <strong>Scikit-Learn y XGBoost</strong>. Para {job.empresa}, eso significa llevar la IA de la demostración a flujos de datos reales, gobernados y medibles.</p>

<p>Logros recientes alineados a su vacante:</p>
<ul>
  <li>{logro1}</li>
  <li>{logro2}</li>
</ul>

<p>Me encantaría explicarles en una conversación de 30 minutos cómo puedo aportar al equipo de {job.empresa}. Quedo atento a su respuesta por correo o por LinkedIn, y agradezco su tiempo y consideración.</p>

<div class="closing">
  <p>Atentamente,</p>
  <div class="signature">
    <p class="name">{self.profile.nombre.upper()}</p>
    <p class="role">{self.profile.titulo}</p>
    <p class="links">
      <a href="mailto:{self.profile.email}">{self.profile.email}</a><span class="sep">|</span><a href="{self.profile.linkedin}">{self.profile.linkedin}</a><span class="sep">|</span><a href="{self.profile.github}">{self.profile.github}</a>
    </p>
  </div>
</div>
</div>
</body>
</html>"""
        return html
    
    def save_documents(self, job: JobPosting, output_dir: Path) -> tuple[Path, Path]:
        """Guarda CV y carta como HTML."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        safe_title = re.sub(r'[^\w\s-]', '', job.titulo).strip().replace(' ', '_')[:50]
        safe_company = re.sub(r'[^\w\s-]', '', job.empresa).strip().replace(' ', '_')[:30]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        cv_path = output_dir / f"CV_{safe_company}_{safe_title}_{timestamp}.html"
        carta_path = output_dir / f"Carta_{safe_company}_{safe_title}_{timestamp}.html"
        
        cv_html = self.generate_cv_html(job)
        carta_html = self.generate_cover_letter_html(job)
        
        cv_path.write_text(cv_html, encoding="utf-8")
        carta_path.write_text(carta_html, encoding="utf-8")
        
        job.cv_adaptado = True
        job.carta_generada = True
        
        return cv_path, carta_path


# ============================
# TRACKER DE APLICACIONES
# ============================

class ApplicationTracker:
    """Gestiona el tracking de aplicaciones en JSONL."""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.applications: list[Application] = []
        self._load()
    
    def _load(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        self.applications.append(Application(**data))
    
    def add(self, app: Application):
        self.applications.append(app)
        self._save()
    
    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for app in self.applications:
                f.write(json.dumps(asdict(app), ensure_ascii=False) + "\n")
    
    def update_status(self, job_id: str, estado: str, nota: str = ""):
        for app in self.applications:
            if app.job_id == job_id:
                app.estado = estado
                if nota:
                    app.seguimiento.append(f"{datetime.now().isoformat()}: {nota}")
                self._save()
                return True
        return False
    
    def get_stats(self) -> dict:
        total = len(self.applications)
        if total == 0:
            return {"total": 0}
        estados = {}
        for app in self.applications:
            estados[app.estado] = estados.get(app.estado, 0) + 1
        return {"total": total, "por_estado": estados}


# ============================
# ORQUESTADOR PRINCIPAL
# ============================

class JobSearchOrchestrator:
    """Orquesta todo el proceso: búsqueda → filtrado → documentos → tracking."""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("output/job_search")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tracker = ApplicationTracker(self.output_dir / "applications.jsonl")
        self.generator = DocumentGenerator(PROFILE)
        
        self.scrapers = {
            "Computrabajo": ComputrabajoScraper(rate_limit=3.0),
            "Elempleo": ElempleoScraper(rate_limit=3.0),
            "Indeed": IndeedScraper(rate_limit=3.0),
            "Google Jobs": GoogleJobsScraper(rate_limit=5.0),
            "LinkedIn": LinkedInScraper(rate_limit=5.0),
        }
    
    async def search_all(self, max_per_platform: int = 20) -> list[JobPosting]:
        """Busca en todas las plataformas en paralelo."""
        all_jobs = []
        
        async with asyncio.TaskGroup() as tg:
            tasks = {}
            for name, scraper in self.scrapers.items():
                tasks[name] = tg.create_task(scraper.search(PROFILE.search_keywords))
            
            for name, task in tasks.items():
                try:
                    jobs = await task
                    # Limitar por plataforma
                    jobs = sorted(jobs, key=lambda j: j.match_score, reverse=True)[:max_per_platform]
                    all_jobs.extend(jobs)
                    print(f"[{name}] {len(jobs)} ofertas encontradas")
                except Exception as e:
                    print(f"[{name}] Error: {e}")
        
        # Deduplicar por URL
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            if job.url not in seen:
                seen.add(job.url)
                unique_jobs.append(job)
        
        # Ordenar por match_score
        unique_jobs.sort(key=lambda j: j.match_score, reverse=True)
        
        print(f"\nTotal ofertas únicas: {len(unique_jobs)}")
        return unique_jobs
    
    def filter_jobs(self, jobs: list[JobPosting]) -> list[JobPosting]:
        """Filtra ofertas según criterios del perfil."""
        filtered = []
        for job in jobs:
            # Filtrar por salario si está disponible
            if job.salario:
                # Intentar extraer número
                nums = re.findall(r'[\d.,]+', job.salario.replace(',', '').replace('.', ''))
                if nums:
                    try:
                        salario = int(nums[0])
                        if salario < PROFILE.salario_min_cop:
                            continue
                    except ValueError:
                        pass
            
            # Filtrar por modalidad
            if job.modalidad and job.modalidad != "No especificada":
                modalidad_lower = job.modalidad.lower()
                if not any(m.lower() in modalidad_lower for m in PROFILE.modalidad):
                    # Permitir si no especifica pero location es Colombia
                    if "colombia" not in job.ubicacion.lower():
                        continue
            
            # Filtrar por match_score mínimo
            if job.match_score < 0.2:
                continue
            
            filtered.append(job)
        
        return filtered
    
    async def generate_documents_for_top(self, jobs: list[JobPosting], top_n: int = 10):
        """Genera CV y carta para los top N jobs."""
        for job in jobs[:top_n]:
            try:
                cv_path, carta_path = self.generator.save_documents(job, self.output_dir / "documents")
                
                # Registrar aplicación
                app = Application(
                    job_id=job.id,
                    fecha=datetime.now().isoformat(),
                    cv_path=str(cv_path),
                    carta_path=str(carta_path),
                    plataforma=job.plataforma,
                )
                self.tracker.add(app)
                
                print(f"✓ Documentos generados: {job.titulo} @ {job.empresa}")
                print(f"  CV: {cv_path.name}")
                print(f"  Carta: {carta_path.name}")
                
            except Exception as e:
                print(f"✗ Error generando docs para {job.titulo}: {e}")
    
    def export_results(self, jobs: list[JobPosting], format: str = "json"):
        """Exporta resultados a JSON/CSV."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            path = self.output_dir / f"jobs_{timestamp}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump([asdict(j) for j in jobs], f, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            import csv
            path = self.output_dir / f"jobs_{timestamp}.csv"
            with open(path, "w", encoding="utf-8", newline="") as f:
                if jobs:
                    writer = csv.DictWriter(f, fieldnames=asdict(jobs[0]).keys())
                    writer.writeheader()
                    for job in jobs:
                        row = asdict(job)
                        # Convertir listas a strings
                        for k, v in row.items():
                            if isinstance(v, list):
                                row[k] = "; ".join(str(x) for x in v)
                        writer.writerow(row)
        
        print(f"Resultados exportados a: {path}")
        return path


# ============================
# CLI / MAIN
# ============================

async def main():
    print("=" * 60)
    print("JOB SEARCH AUTOMATION — AI_Nexus_Core")
    print(f"Perfil: {PROFILE.nombre} | {PROFILE.titulo}")
    print(f"Salario objetivo: ≥ {PROFILE.salario_min_cop:,} COP")
    print(f"Modalidad: {', '.join(PROFILE.modalidad)}")
    print("=" * 60)
    
    orchestrator = JobSearchOrchestrator()
    
    # 1. Buscar en todas las plataformas
    print("\n🔍 Buscando ofertas en todas las plataformas...")
    jobs = await orchestrator.search_all(max_per_platform=15)
    
    # 2. Filtrar según criterios
    print("\n🎯 Filtrando según criterios del perfil...")
    filtered = orchestrator.filter_jobs(jobs)
    print(f"Ofertas tras filtro: {len(filtered)}")
    
    # 3. Mostrar top 10
    print("\n📋 Top 10 ofertas:")
    for i, job in enumerate(filtered[:10], 1):
        print(f"  {i}. {job.titulo} @ {job.empresa}")
        print(f"     📍 {job.ubicacion} | 💰 {job.salario or 'No especificado'} | 🏠 {job.modalidad}")
        print(f"     🎯 Match: {job.match_score:.1%} | 🌐 {job.plataforma}")
        print(f"     🔗 {job.url[:80]}...")
    
    # 4. Generar documentos para top 10
    print("\n📄 Generando CV y cartas adaptadas para top 10...")
    await orchestrator.generate_documents_for_top(filtered, top_n=10)
    
    # 5. Exportar resultados
    print("\n💾 Exportando resultados...")
    orchestrator.export_results(filtered, "json")
    orchestrator.export_results(filtered, "csv")
    
    # 6. Stats
    stats = orchestrator.tracker.get_stats()
    print(f"\n📊 Stats: {stats}")
    
    print("\n✅ Proceso completado. Revisa la carpeta 'output/job_search/'")
    print("   - documents/: CV y cartas HTML listos para convertir a PDF")
    print("   - jobs_*.json/csv: Lista completa de ofertas")
    print("   - applications.jsonl: Tracking de aplicaciones")


if __name__ == "__main__":
    asyncio.run(main())