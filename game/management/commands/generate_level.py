import random
import json
from django.core.management.base import BaseCommand
from game.models import GameLevel

class PerfectFlowGenerator:
    def __init__(self, size, num_colors):
        self.size = size
        self.num_colors = num_colors
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        
    def generate(self):
        full_path = self.find_hamiltonian_path(random.randint(0, self.size-1), random.randint(0, self.size-1), [])
        if not full_path:
            self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
            return self.generate()

        segments = []
        remaining_path = full_path
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta", "lime", "brown"]

        for i in range(self.num_colors - 1):
            max_break = len(remaining_path) - (self.num_colors - i - 1) * 2
            break_point = random.randint(2, max_break) if max_break > 2 else 2
            segments.append(remaining_path[:break_point])
            remaining_path = remaining_path[break_point:]
        
        segments.append(remaining_path)
        dot_config = {}
        for i, sub_path in enumerate(segments):
            color = colors[i % len(colors)]
            start_node, end_node = sub_path[0], sub_path[-1]
            dot_config[f"{start_node[0]+1}{start_node[1]+1}"] = color
            dot_config[f"{end_node[0]+1}{end_node[1]+1}"] = color
            
        return dot_config

    def find_hamiltonian_path(self, r, c, path):
        path.append((r, c))
        self.grid[r][c] = True
        if len(path) == self.size * self.size: return path
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        random.shuffle(neighbors)
        for nr, nc in neighbors:
            if 0 <= nr < self.size and 0 <= nc < self.size and not self.grid[nr][nc]:
                result = self.find_hamiltonian_path(nr, nc, path[:])
                if result: return result
        self.grid[r][c] = False
        return None

class Command(BaseCommand):
    help = 'Generates perfect Flow levels dynamically'

    def add_arguments(self, parser):
        parser.add_argument('size', type=int, help='Grid size (5, 6, 8)')
        parser.add_argument('count', type=int, help='Number of levels to generate')
        parser.add_argument('--colors', type=int, default=5, help='Number of colors/paths')

    def handle(self, *args, **options):
        size = options['size']
        count = options['count']
        num_colors = options['colors']

        self.stdout.write(f"Generating {count} levels for {size}x{size} grid...")

        for i in range(count):
            gen = PerfectFlowGenerator(size, num_colors)
            config = gen.generate()
            
            # Database mein save karna
            GameLevel.objects.create(
                level_number=i + 1, # Isko aap logic ke hisab se change kar sakte hain
                size=size,
                dot_configuration=config # Agar JSONField hai toh direct, warna json.dumps(config)
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} levels!'))