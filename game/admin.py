import random
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect
from django.db.models import Max
from .models import GameLevel

# --- 1. AAPKA PERFECT PATH GENERATOR LOGIC (NO CHANGES) ---
class PerfectFlowGenerator:
    def __init__(self, size=5, num_colors=5):
        self.size = size
        self.num_colors = num_colors
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        
    def generate(self):
        full_path = self.find_hamiltonian_path(0, 0, [])
        if not full_path:
            self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
            return self.generate()

        dot_config = {}
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta", "lime"]
        segments = []
        remaining_path = full_path
        
        for i in range(self.num_colors - 1):
            max_break = len(remaining_path) - (self.num_colors - i - 1) * 2
            break_point = random.randint(2, max_break) if max_break > 2 else 2
            segments.append(remaining_path[:break_point])
            remaining_path = remaining_path[break_point:]
        
        segments.append(remaining_path)

        for i, sub_path in enumerate(segments):
            color = colors[i % len(colors)]
            start_node = sub_path[0]
            end_node = sub_path[-1]
            dot_config[f"{start_node[0]+1}{start_node[1]+1}"] = color
            dot_config[f"{end_node[0]+1}{end_node[1]+1}"] = color
        return dot_config

    def find_hamiltonian_path(self, r, c, path):
        path.append((r, c))
        self.grid[r][c] = True
        if len(path) == self.size * self.size:
            return path
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        random.shuffle(neighbors)
        for nr, nc in neighbors:
            if 0 <= nr < self.size and 0 <= nc < self.size and not self.grid[nr][nc]:
                result = self.find_hamiltonian_path(nr, nc, path[:])
                if result: return result
        self.grid[r][c] = False
        return None

# --- 2. ADMIN CONFIGURATION ---
@admin.register(GameLevel)
class GameLevelAdmin(admin.ModelAdmin):
    # list_display fix kiya: grid_size aur level_number
    list_display = ('level_number', 'grid_size', 'created_at')
    list_filter = ('grid_size',)
    change_list_template = "admin/game_level_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('gen-5/', self.generate_5x5, name='gen-5'),
            path('gen-6/', self.generate_6x6, name='gen-6'),
            path('gen-8/', self.generate_8x8, name='gen-8'),
        ]
        return custom_urls + urls

    def bulk_generate(self, size, colors):
        # Specific grid_size ke liye aakhri level number check karna
        last_level_data = GameLevel.objects.filter(grid_size=size).aggregate(Max('level_number'))
        last_level = last_level_data['level_number__max'] or 0
        
        levels_created = 0
        for i in range(1, 101):
            gen = PerfectFlowGenerator(size, colors)
            config = gen.generate()
            
            # Aapke model fields ke hisab se data save
            GameLevel.objects.create(
                grid_size=size,
                level_number=last_level + i,
                dot_configuration=config
            )
            levels_created += 1
        return levels_created

    # Button handlers
    def generate_5x5(self, request):
        count = self.bulk_generate(5, 5)
        self.message_user(request, f"Gazab! 5x5 ke {count} naye levels level {GameLevel.objects.filter(grid_size=5).count()} tak pahunch gaye.", messages.SUCCESS)
        return redirect("..")

    def generate_6x6(self, request):
        count = self.bulk_generate(6, 6)
        self.message_user(request, f"Medium (6x6) ke {count} naye levels add ho gaye.", messages.SUCCESS)
        return redirect("..")

    def generate_8x8(self, request):
        count = self.bulk_generate(8, 8)
        self.message_user(request, f"Hard (8x8) ke {count} naye levels database mein store ho gaye.", messages.SUCCESS)
        return redirect("..")