# -*- coding: utf-8 -*-
"""Contenido del currículum de Fernanda Ramos, en español e inglés.

Fuente única para el PDF y el Word. TODO sale del currículum que entregó (CV_Fernanda_Ramos_Spanish.pdf):
no se añadió ni un dato, ni una cifra, ni un logro. Lo que cambia es la forma:
 · los puestos van en femenino, como ella misma se nombra en su perfil («Consultora»);
 · «Universidad de Valle de México» se escribe con su nombre oficial, «del Valle»;
 · las listas de alcance de Freyr y Mino Labs se conservan como ella las escribió (son ámbitos, no logros:
   convertirlas en verbos sería ponerle palabras en la boca);
 · las competencias van agrupadas en renglones «rótulo: valores» para que un lector automático no pierda
   qué va con qué.
Siglas que no se expanden en inglés porque no hay una sola lectura segura: BPD, BPAD, CEMAR, LGSMP.
"""

DATOS = {
    "nombre": "Fernanda Ramos",
    "tel": "+52 442 436 3203",
    "tel_href": "tel:+524424363203",
    "correo": "maferabe.1651@gmail.com",
}

ES = {
    "lang": "es",
    "titulo": "Asuntos Regulatorios",
    "bajada": "Químico Farmacéutico Biotecnólogo · Maestría en Gestión de la Calidad",
    "h_perfil": "Perfil profesional",
    "perfil": ("Consultora con 4 años de experiencia en asuntos regulatorios para la industria farmacéutica (OTC, biológicos, "
               "biotecnológicos, herbolarios y vitamínicos), dispositivos médicos (clase I, II y III), suplementos alimenticios, "
               "remedios herbolarios y cosméticos. Especialista en trámites ante COFEPRIS, registro sanitario, prórrogas y "
               "normatividad vigente en México y LATAM. Manejo de BPM, BPD, ISO 9001, ISO 13485 y BPAD, con certificación como "
               "auditora interna y en sistemas de gestión de la calidad."),
    "h_comp": "Competencias",
    "comp": [
        ("Productos", "medicamentos (OTC, farmoquímicos, biológicos, biotecnológicos, herbolarios, vitamínicos), dispositivos médicos clase I, II y III, suplementos alimenticios, remedios herbolarios y cosméticos"),
        ("Trámites", "COFEPRIS, VUCEM y FDA (21 CFR 820) · registro sanitario y prórrogas · permiso previo de importación · consultas de clasificación"),
        ("Calidad y normas", "BPM, BPD, BPAD · ISO 9001, ISO 13485, ISO 19011 · LGS, RIS · NOM-241, NOM-240, NOM-073, NOM-072, NOM-248, NOM-251"),
        ("Habilidades", "gestión de solicitudes y sometimientos regulatorios, gestión de proyectos, pensamiento estratégico, comunicación, sensibilidad intercultural, atención al detalle y cumplimiento de plazos"),
    ],
    "h_exp": "Experiencia profesional",
    "exp": [
        {"puesto": "Regulatory Affairs Delivery Specialist", "empresa": "Freyr Life Sciences, S. de R.L. de C.V.", "fechas": "Jun 2024 – Actualidad",
         "area": "Consultoría y estrategia regulatoria", "puntos": [
            "Medicamentos (farmoquímicos, herbolarios, biológicos y biotecnológicos) y CMN.",
            "Dispositivos médicos (clase I, II y III), suplementos alimenticios y cosméticos.",
            "Trámites ante COFEPRIS y VUCEM; farmacovigilancia y tecnovigilancia (CEMAR).",
            "Publicidad (LGSMP), importación y exportación.",
            "Acompañamiento y asesoría al equipo en el lanzamiento de productos, su distribución y marketing.",
            "Auditorías internas y sistema de gestión de la calidad.",
        ]},
        {"puesto": "Coordinadora de Asuntos Regulatorios", "empresa": "Mino Labs, S.A. de C.V.", "fechas": "Feb 2023 – Actualidad",
         "area": "Consultoría y estrategia regulatoria", "puntos": [
            "Medicamentos (farmoquímicos, herbolarios y biológicos) y CMN.",
            "Dispositivos médicos (clase I, II y III), suplementos alimenticios y cosméticos.",
            "Trámites ante COFEPRIS; farmacovigilancia y tecnovigilancia.",
            "Publicidad, importación y exportación.",
            "Acompañamiento y asesoría al equipo en el lanzamiento de productos, su distribución y marketing.",
            "Auditorías internas.",
        ]},
        {"puesto": "Consultora Regulatoria Externa LATAM", "empresa": "Herbion International Inc., Estados Unidos", "fechas": "Sep 2022 – Abr 2023",
         "area": "Manufactura de suplementos alimenticios y remedios herbolarios", "puntos": [
            "Trámites ante COFEPRIS.",
            "Elaboración del dossier para la solicitud de registro sanitario de remedios herbolarios y traducción de documentos.",
            "Revisión de fórmula cuali-cuantitativa y consultas de clasificación.",
            "Permiso previo de importación de productos y servicios.",
            "Normatividad: LGS, RIS, NOM-251, NOM-248 y NOM-072.",
        ]},
        {"puesto": "Analista de Asuntos Regulatorios y Aseguramiento de la Calidad", "empresa": "Truemed, S.A. de C.V.", "fechas": "Dic 2020 – Sep 2022",
         "area": "Manufactura de dispositivos médicos", "puntos": [
            "Trámites ante COFEPRIS y FDA (21 CFR 820, Quality System Regulation); registro sanitario de dispositivos médicos y tecnovigilancia.",
            "Normas NOM-241, NOM-073, NOM-240, ISO 9001, ISO 19011, ISO 13485, BPM y BPD.",
            "Seguimiento y cierre de acciones correctivas (Ishikawa, 5 porqués); procedimientos normalizados de operación (PNO) y mapeo de procesos.",
            "Auditora interna y participación activa en el proceso de certificación ISO 13485 por BSI Group.",
            "Órdenes de producción, inspección de producto semiterminado y terminado, liberación de lotes y facturación.",
        ]},
    ],
    "h_edu": "Formación académica",
    "edu": [
        ("Maestría en Gestión de la Calidad", "Universidad del Valle de México", "2024"),
        ("Licenciatura: Químico Farmacéutico Biotecnólogo", "Universidad del Valle de México", "2019"),
    ],
    "h_cert": "Certificaciones",
    "cert": [
        ("Diplomado en Regulación Sanitaria para la Industria Farmacéutica", "INEDUFARM", "Ago 2025 – en curso"),
        ("Diplomado en Registro Sanitario LATAM (México, Brasil, Colombia, Ecuador, Chile y CAM)", "INEDUFARM", "Jun 2023"),
        ("Certificación en Armado de Dossier de Dispositivos Médicos", "Regulate", "Abr 2023"),
        ("Certificación en Trámites ante COFEPRIS", "Regulate", "Abr 2023"),
        ("Curso de Suplementos Alimenticios: requisitos regulatorios para su comercialización", "AMEPRES", "Oct 2022"),
        ("Certificación ISO 19011: Formación de Auditores Internos de Sistemas de Gestión", "Instituto Mexicano de Consultoría y Capacitación Integral", "Ago 2021"),
        ("Certificación ISO 9001:2015: Implementación de un Sistema de Gestión de Calidad", "Instituto Mexicano de Consultoría y Capacitación Integral", "Ago 2021"),
    ],
    "h_idi": "Idiomas",
    "idi": [("Inglés", "C2, avanzado"), ("Alemán", "B2, intermedio · certificado Goethe-Institut")],
}

EN = {
    "lang": "en",
    "titulo": "Regulatory Affairs",
    "bajada": "B.Sc. Pharmaceutical Biotechnology Chemistry · Master’s in Quality Management",
    "h_perfil": "Professional profile",
    "perfil": ("Consultant with 4 years of experience in regulatory affairs for the pharmaceutical industry (OTC, biologics, "
               "biotechnology, herbal and vitamin products), medical devices (Class I, II and III), food supplements, herbal "
               "remedies and cosmetics. Specialised in filings before COFEPRIS, sanitary registration, renewals and current "
               "regulations in Mexico and LATAM. Working knowledge of GMP, BPD, ISO 9001, ISO 13485 and BPAD, certified as an "
               "internal auditor and in quality management systems."),
    "h_comp": "Core competencies",
    "comp": [
        ("Products", "medicines (OTC, small-molecule, biologics, biotechnology, herbal, vitamin), Class I, II and III medical devices, food supplements, herbal remedies and cosmetics"),
        ("Filings", "COFEPRIS, VUCEM and FDA (21 CFR 820) · sanitary registration and renewals · prior import permits · classification enquiries"),
        ("Quality and standards", "GMP, BPD, BPAD · ISO 9001, ISO 13485, ISO 19011 · LGS, RIS · NOM-241, NOM-240, NOM-073, NOM-072, NOM-248, NOM-251"),
        ("Skills", "application filing, regulatory submissions, project management, strategic thinking, communication, cultural awareness, attention to detail and timelines"),
    ],
    "h_exp": "Professional experience",
    "exp": [
        {"puesto": "Regulatory Affairs Delivery Specialist", "empresa": "Freyr Life Sciences, S. de R.L. de C.V.", "fechas": "Jun 2024 – Present",
         "area": "Regulatory consulting and strategy", "puntos": [
            "Medicines (small-molecule, herbal, biologics and biotechnology) and the New Molecules Committee (CMN).",
            "Medical devices (Class I, II and III), food supplements and cosmetics.",
            "Filings before COFEPRIS and VUCEM; pharmacovigilance and technovigilance (CEMAR).",
            "Advertising (LGSMP), import and export.",
            "Support and advice to the team on product launch, distribution and marketing.",
            "Internal audits and quality management system.",
        ]},
        {"puesto": "Regulatory Affairs Coordinator", "empresa": "Mino Labs, S.A. de C.V.", "fechas": "Feb 2023 – Present",
         "area": "Regulatory consulting and strategy", "puntos": [
            "Medicines (small-molecule, herbal and biologics) and the New Molecules Committee (CMN).",
            "Medical devices (Class I, II and III), food supplements and cosmetics.",
            "Filings before COFEPRIS; pharmacovigilance and technovigilance.",
            "Advertising, import and export.",
            "Support and advice to the team on product launch, distribution and marketing.",
            "Internal audits.",
        ]},
        {"puesto": "External Regulatory Consultant, LATAM", "empresa": "Herbion International Inc., United States", "fechas": "Sep 2022 – Apr 2023",
         "area": "Manufacturer of food supplements and herbal remedies", "puntos": [
            "Filings before COFEPRIS.",
            "Preparation of the dossier for the sanitary registration of herbal remedies, and translation of documents.",
            "Review of qualitative-quantitative formulas and classification enquiries.",
            "Prior import permits for products and services.",
            "Regulations: LGS, RIS, NOM-251, NOM-248 and NOM-072.",
        ]},
        {"puesto": "Regulatory Affairs and Quality Assurance Analyst", "empresa": "Truemed, S.A. de C.V.", "fechas": "Dec 2020 – Sep 2022",
         "area": "Medical device manufacturer", "puntos": [
            "Filings before COFEPRIS and FDA (21 CFR 820, Quality System Regulation); sanitary registration of medical devices and technovigilance.",
            "Standards NOM-241, NOM-073, NOM-240, ISO 9001, ISO 19011, ISO 13485, GMP and BPD.",
            "Follow-up and closure of corrective actions (Ishikawa, 5 Whys); standard operating procedures (SOPs) and process mapping.",
            "Internal auditor, and active participation in the ISO 13485 certification process by BSI Group.",
            "Production orders, inspection of semi-finished and finished product, batch release and invoicing.",
        ]},
    ],
    "h_edu": "Education",
    "edu": [
        ("Master’s Degree in Quality Management", "Universidad del Valle de México", "2024"),
        ("Bachelor’s Degree in Pharmaceutical Biotechnology Chemistry (Químico Farmacéutico Biotecnólogo)", "Universidad del Valle de México", "2019"),
    ],
    "h_cert": "Certifications",
    "cert": [
        ("Diploma in Sanitary Regulation for the Pharmaceutical Industry", "INEDUFARM", "Aug 2025 – in progress"),
        ("Diploma in LATAM Sanitary Registration (Mexico, Brazil, Colombia, Ecuador, Chile and Central America)", "INEDUFARM", "Jun 2023"),
        ("Certification in Medical Device Dossier Preparation", "Regulate", "Apr 2023"),
        ("Certification in COFEPRIS Filings", "Regulate", "Apr 2023"),
        ("Course on Food Supplements: regulatory requirements for marketing", "AMEPRES", "Oct 2022"),
        ("ISO 19011 Certification: Internal Auditor Training for Management Systems", "Instituto Mexicano de Consultoría y Capacitación Integral", "Aug 2021"),
        ("ISO 9001:2015 Certification: Implementing a Quality Management System", "Instituto Mexicano de Consultoría y Capacitación Integral", "Aug 2021"),
    ],
    "h_idi": "Languages",
    "idi": [("English", "C2, advanced"), ("German", "B2, intermediate · Goethe-Institut certificate")],
}
