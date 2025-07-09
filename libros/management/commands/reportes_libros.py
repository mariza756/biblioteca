import os
import matplotlib.pyplot as plt
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libros.models import Autor, Genero, Libro, Calificacion
from django.db.models import Count, Avg

plt.rcParams.update({'font.size': 12})  # Tamaño de fuente global

def add_labels(ax, rects):
    """Agrega etiquetas de valor encima de las barras."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}' if isinstance(height, float) else f'{int(height)}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

class Command(BaseCommand):
    help = 'Genera reportes gráficos de libros, autores y calificaciones'

    def handle(self, *args, **options):
        # Crear carpeta 'graficos' si no existe
        self.output_dir = "graficos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.reporte1_libros_por_genero()
        self.reporte2_top_autores_mas_libros()
        self.reporte3_top_libros_mejor_calificados()
        self.reporte_libros_por_anio()
        self.reporte5_top_usuarios_mas_calificaciones()
        self.reporte6_distribucion_calificaciones()
        self.reporte7_libros_sin_calificaciones()
        self.reporte8_top_autores_mejor_calificados()
        self.reporte9_top_generos_mas_calificados()
        self.reporte10_top_libros_mas_calificados()
        self.stdout.write(self.style.SUCCESS('¡Todos los reportes fueron generados en la carpeta graficos!'))

    def reporte1_libros_por_genero(self):
        data = Genero.objects.annotate(num_libros=Count('libros')).order_by('-num_libros')[:5]
        fig, ax = plt.subplots(figsize=(8,6))  # <-- ¡Aumenta tamaño de figura!
        bars = ax.bar([g.nombre for g in data], [g.num_libros for g in data], color='#4B8BBE')
        add_labels(ax, bars)
        ax.set_title('Top 5 géneros con más libros', fontsize=16, fontweight='bold')
        ax.set_ylabel('Cantidad de libros')
        ax.set_xlabel('Género')
        plt.xticks(rotation=35, ha='right', fontsize=12)
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte1_top5_libros_por_genero.png'))
        plt.close(fig)


    def reporte2_top_autores_mas_libros(self):
        data = Autor.objects.annotate(num_libros=Count('libros')).order_by('-num_libros')[:5]
        fig, ax = plt.subplots(figsize=(8,6))
        valores = [a.num_libros for a in data]
        autores = [a.nombre for a in data]
        bars = ax.bar(autores, valores, color='#306998')

        # Etiquetas arriba de la barra
        for rect in bars:
            height = rect.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 8),  # Más separación vertical
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Subir el límite superior del eje Y un 10%
        ax.set_ylim(0, max(valores)*1.15)
        ax.set_title('Top 5 autores con más libros', fontsize=16, fontweight='bold')
        ax.set_ylabel('Cantidad de libros')
        ax.set_xlabel('Autor')
        plt.xticks(rotation=30, ha='right', fontsize=12)
        plt.tight_layout(pad=2.5)
        plt.savefig(os.path.join(self.output_dir, 'reporte2_top5_autores_mas_libros.png'))
        plt.close(fig)


    def reporte3_top_libros_mejor_calificados(self):
        data = Libro.objects.annotate(
            prom_calif=Avg('calificaciones__calificacion')
        ).filter(prom_calif__isnull=False).order_by('-prom_calif')[:5]
        fig, ax = plt.subplots(figsize=(10, 6))  # Más ancho para nombres largos
        valores = [float(round(l.prom_calif, 2)) for l in data]
        titulos = [l.titulo for l in data]
        bars = ax.bar(titulos, valores, color='#FFB000')

        # Etiquetas encima de cada barra
        for rect in bars:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 8),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=12, fontweight='bold')

        # Ajustar límites Y para que las etiquetas no se peguen al borde
        ax.set_ylim(1, max(valores)*1.15)

        ax.set_title('Top 5 libros mejor calificados', fontsize=16, fontweight='bold', pad=25)
        ax.set_ylabel('Calificación promedio (1 a 5)')
        ax.set_xlabel('Libro')
        plt.xticks(rotation=30, ha='right', fontsize=12)
        plt.tight_layout(pad=3.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte3_top5_libros_mejor_calificados.png'))
        plt.close(fig)


    def reporte_libros_por_anio(self):
        from django.db.models.functions import ExtractYear
        data = Libro.objects.annotate(anio=ExtractYear('fecha_lanzamiento')) \
            .values('anio').annotate(total=Count('id')).order_by('anio')
        
        anios = [str(d['anio']) for d in data]
        cantidades = [d['total'] for d in data]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(anios, cantidades, marker='o', linestyle='-', color='#306998', linewidth=2)

        # Etiquetas de valor encima de cada punto
        for i, v in enumerate(cantidades):
            ax.annotate(str(v), (anios[i], cantidades[i]), textcoords="offset points",
                        xytext=(0,8), ha='center', fontsize=11, fontweight='bold')

        ax.set_title('Libros publicados por año', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Cantidad de libros')
        ax.set_xlabel('Año')
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte4_libros_por_anio.png'))
        plt.close(fig)


    def reporte5_top_usuarios_mas_calificaciones(self):
        data = User.objects.annotate(num_calif=Count('calificaciones')).order_by('-num_calif')[:5]
        fig, ax = plt.subplots(figsize=(9, 6))
        valores = [u.num_calif for u in data]
        usuarios = [u.username for u in data]
        bars = ax.bar(usuarios, valores, color='#E06F12')

        # Etiquetas arriba de cada barra, bien separadas
        for rect in bars:
            height = rect.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 8),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=11)

        ax.set_ylim(0, max(valores)*1.13)  # 13% más de espacio arriba
        ax.set_title('Top 5 usuarios con más calificaciones', fontsize=16, fontweight='bold', pad=18)
        ax.set_ylabel('Cantidad de calificaciones')
        ax.set_xlabel('Usuario')
        plt.xticks(rotation=25, ha='right', fontsize=12)
        plt.tight_layout(pad=2.5)
        plt.savefig(os.path.join(self.output_dir, 'reporte5_top5_usuarios_mas_calificaciones.png'))
        plt.close(fig)


    def reporte6_distribucion_calificaciones(self):
        import numpy as np
        califs = list(Calificacion.objects.values_list('calificacion', flat=True))
        califs = [c for c in califs if 1.0 <= c <= 5.0]  # Solo calificaciones válidas
        fig, ax = plt.subplots()
        bins = np.arange(0.5, 6.5, 1)
        n, bins_, patches = ax.hist(califs, bins=bins, edgecolor='black', rwidth=0.85, color='#7FB77E')
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xlim(0.5, 5.5)
        ax.set_title('Distribución de calificaciones (1 a 5)', fontsize=15, fontweight='bold')
        ax.set_xlabel('Calificación')
        ax.set_ylabel('Cantidad')
        for i in range(len(n)):
            ax.text(bins[i] + 0.5, n[i], int(n[i]), ha='center', va='bottom', fontsize=10, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'reporte6_distribucion_calificaciones.png'))
        plt.close(fig)

    def reporte7_libros_sin_calificaciones(self):
        data = Libro.objects.annotate(num_calif=Count('calificaciones')).filter(num_calif=0)
        titulos = [l.titulo for l in data]

        if not titulos:
            # Si no hay libros sin calificaciones, genera imagen indicándolo
            fig, ax = plt.subplots(figsize=(6, 2))
            ax.text(0.5, 0.5, 'Todos los libros tienen al menos una calificación', ha='center', va='center', fontsize=15)
            ax.axis('off')
        else:
            # Hacer una tabla de libros
            fig, ax = plt.subplots(figsize=(10, len(titulos)*0.4+1))
            table_data = [[titulo] for titulo in titulos]
            ax.table(cellText=table_data, colLabels=['Libro sin calificación'], loc='center', cellLoc='left')
            ax.axis('off')
            ax.set_title('Libros sin calificaciones', fontsize=15, fontweight='bold', pad=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'reporte7_libros_sin_calificaciones.png'))
        plt.close(fig)


    def reporte8_top_autores_mejor_calificados(self):
        data = Autor.objects.annotate(
            prom_autor=Avg('libros__calificaciones__calificacion')
        ).filter(prom_autor__isnull=False).order_by('-prom_autor')[:5]
        autores = [a.nombre for a in data]
        valores = [float(round(a.prom_autor, 2)) for a in data]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.barh(autores, valores, color='#008891')
        
        for rect in bars:
            width = rect.get_width()
            ax.annotate(f'{width:.2f}',
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(8, 0),
                        textcoords="offset points",
                        ha='left', va='center', fontsize=12, fontweight='bold')

        ax.set_xlim(1, max(valores)*1.15)
        ax.set_xlabel('Calificación promedio (1 a 5)')
        ax.set_ylabel('Autor')
        ax.set_title('Top 5 autores mejor calificados', fontsize=16, fontweight='bold', pad=16)
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte8_top5_autores_mejor_calificados.png'))
        plt.close(fig)

    def reporte9_top_generos_mas_calificados(self):
        data = Genero.objects.annotate(
            total_calif=Count('libros__calificaciones')
        ).order_by('-total_calif')[:5]
        generos = [g.nombre for g in data]
        valores = [g.total_calif for g in data]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.barh(generos, valores, color='#9A1750')

        for rect in bars:
            width = rect.get_width()
            ax.annotate(f'{int(width)}',
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(8, 0),
                        textcoords="offset points",
                        ha='left', va='center', fontsize=12, fontweight='bold')

        ax.set_xlabel('Cantidad de calificaciones')
        ax.set_ylabel('Género')
        ax.set_title('Top 5 géneros más calificados', fontsize=16, fontweight='bold', pad=16)
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte9_top5_generos_mas_calificados.png'))
        plt.close(fig)


    def reporte10_top_libros_mas_calificados(self):
        data = Libro.objects.annotate(
            total_calif=Count('calificaciones')
        ).order_by('-total_calif')[:5]
        titulos = [l.titulo for l in data]
        valores = [l.total_calif for l in data]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.barh(titulos, valores, color='#E23E57')

        for rect in bars:
            width = rect.get_width()
            ax.annotate(f'{int(width)}',
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(8, 0),
                        textcoords="offset points",
                        ha='left', va='center', fontsize=12, fontweight='bold')

        ax.set_xlabel('Cantidad de calificaciones')
        ax.set_ylabel('Libro')
        ax.set_title('Top 5 libros más calificados', fontsize=16, fontweight='bold', pad=16)
        plt.tight_layout(pad=2.0)
        plt.savefig(os.path.join(self.output_dir, 'reporte10_top5_libros_mas_calificados.png'))
        plt.close(fig)
