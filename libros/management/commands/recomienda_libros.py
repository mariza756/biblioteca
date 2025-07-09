from django.core.management.base import BaseCommand
from libros.models import Libro, Genero
from django.db.models import Avg, Count

class Command(BaseCommand):
    help = "Recomienda los mejores libros de un género seleccionado (por id o nombre)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--genero',
            type=str,
            help="ID o nombre del género para recomendaciones"
        )
        parser.add_argument(
            '--top',
            type=int,
            default=3,
            help="Cantidad de libros a recomendar (por defecto 3)"
        )

    def handle(self, *args, **options):
        top_n = options['top']
        arg_genero = options['genero']

        if arg_genero:
            # ¿Es un id (número)? Si no, intenta por nombre
            try:
                genero = Genero.objects.get(id=int(arg_genero))
            except ValueError:
                # No es número, intenta por nombre (case insensitive)
                try:
                    genero = Genero.objects.get(nombre__iexact=arg_genero)
                except Genero.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Género '{arg_genero}' no encontrado."))
                    return
            except Genero.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Género con id={arg_genero} no encontrado."))
                return
        else:
            # Mostrar géneros disponibles
            generos = Genero.objects.all().order_by('id')
            self.stdout.write("Géneros disponibles:")
            for g in generos:
                self.stdout.write(f"{g.id}. {g.nombre}")
            self.stdout.write("")
            seleccion = input("Seleccione el ID del género: ")
            try:
                genero = Genero.objects.get(id=int(seleccion))
            except (ValueError, Genero.DoesNotExist):
                self.stdout.write(self.style.ERROR("Selección inválida."))
                return

        # Recomendaciones
        libros = Libro.objects.filter(genero=genero).annotate(
            prom_calif=Avg('calificaciones__calificacion'),
            total_calif=Count('calificaciones')
        ).filter(prom_calif__isnull=False).order_by('-prom_calif', '-total_calif')[:top_n]

        if not libros:
            self.stdout.write(self.style.WARNING(
                f"No hay libros calificados en el género '{genero.nombre}'."
            ))
            return

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"📚 Recomendaciones de libros en el género '{genero.nombre}':"
        ))
        for i, libro in enumerate(libros, 1):
            self.stdout.write(
                f"{i}. {libro.titulo} — Promedio: {libro.prom_calif:.2f} "
                f"({libro.total_calif} calificaciones) [Autor: {libro.autor.nombre}]"
            )

        # Opcional: guardar a archivo
        with open('recomendaciones_libros.txt', 'w', encoding='utf-8') as f:
            f.write(f"Recomendaciones de libros en el género '{genero.nombre}':\n")
            for i, libro in enumerate(libros, 1):
                f.write(
                    f"{i}. {libro.titulo} — Promedio: {libro.prom_calif:.2f} "
                    f"({libro.total_calif} calificaciones) [Autor: {libro.autor.nombre}]\n"
                )
        self.stdout.write(self.style.SUCCESS("También se guardó la recomendación en 'recomendaciones_libros.txt'."))
