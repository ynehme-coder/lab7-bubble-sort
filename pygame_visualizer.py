"""2D Bubble Sort visualization using pygame.

Controls:
- SPACE: start/pause animation
- R: reset with a new random list
- UP/DOWN: speed up or slow down
- ESC or window close: quit
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 620
TOP_MARGIN = 80
SIDE_MARGIN = 30
BAR_GAP = 4
DEFAULT_SIZE = 20
MIN_VALUE = 10
MAX_VALUE = 100


@dataclass
class SortEvent:
	kind: str
	values: list[int]
	left: int | None = None
	right: int | None = None
	sorted_from: int | None = None


def bubble_sort_events(values: list[int]):
	"""Yield sorting events so the renderer can animate each algorithm step."""
	arr = values.copy()
	n = len(arr)

	for i in range(n):
		swapped = False

		for j in range(0, n - 1 - i):
			# Show the current comparison before deciding whether to swap.
			yield SortEvent(kind="compare", values=arr.copy(), left=j, right=j + 1)

			if arr[j] > arr[j + 1]:
				arr[j], arr[j + 1] = arr[j + 1], arr[j]
				swapped = True
				# Show the list immediately after each swap.
				yield SortEvent(kind="swap", values=arr.copy(), left=j, right=j + 1)

		# The suffix from n - i - 1 to end is sorted after each pass.
		sorted_from = n - i - 1
		yield SortEvent(kind="pass_complete", values=arr.copy(), sorted_from=sorted_from)

		if not swapped:
			# No swaps means the remaining prefix is already sorted.
			yield SortEvent(kind="done", values=arr.copy(), sorted_from=0)
			return

	yield SortEvent(kind="done", values=arr.copy(), sorted_from=0)


class BubbleSortVisualizer:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption("Bubble Sort 2D Visualizer")
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()

		self.font = pygame.font.SysFont("consolas", 22)
		self.small_font = pygame.font.SysFont("consolas", 18)

		self.running = True
		self.playing = False
		self.step_delay_ms = 140
		self.last_step_time = 0

		self.values = self._new_values()
		self.events = bubble_sort_events(self.values)

		self.active_left: int | None = None
		self.active_right: int | None = None
		self.sorted_from: int | None = None
		self.finished = False

	def _new_values(self) -> list[int]:
		return [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(DEFAULT_SIZE)]

	def reset(self) -> None:
		self.values = self._new_values()
		self.events = bubble_sort_events(self.values)
		self.active_left = None
		self.active_right = None
		self.sorted_from = None
		self.finished = False
		self.playing = False

	def handle_events(self) -> None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_SPACE:
					if not self.finished:
						self.playing = not self.playing
				elif event.key == pygame.K_r:
					self.reset()
				elif event.key == pygame.K_UP:
					# Smaller delay means faster animation.
					self.step_delay_ms = max(10, self.step_delay_ms - 10)
				elif event.key == pygame.K_DOWN:
					self.step_delay_ms = min(600, self.step_delay_ms + 10)

	def advance_sort(self) -> None:
		if not self.playing or self.finished:
			return

		now = pygame.time.get_ticks()
		if now - self.last_step_time < self.step_delay_ms:
			return
		self.last_step_time = now

		try:
			event = next(self.events)
		except StopIteration:
			self.finished = True
			self.playing = False
			self.active_left = None
			self.active_right = None
			self.sorted_from = 0
			return

		self.values = event.values
		self.active_left = event.left
		self.active_right = event.right

		if event.kind == "pass_complete":
			self.sorted_from = event.sorted_from
			self.active_left = None
			self.active_right = None
		elif event.kind == "done":
			self.sorted_from = 0
			self.finished = True
			self.playing = False
			self.active_left = None
			self.active_right = None

	def draw(self) -> None:
		self.screen.fill((18, 24, 38))

		title = self.font.render("Bubble Sort Visualizer", True, (236, 242, 255))
		self.screen.blit(title, (SIDE_MARGIN, 16))

		subtitle = self.small_font.render(
			"SPACE start/pause | R reset | UP/DOWN speed | ESC quit",
			True,
			(168, 184, 214),
		)
		self.screen.blit(subtitle, (SIDE_MARGIN, 46))

		speed_text = self.small_font.render(
			f"Delay: {self.step_delay_ms} ms", True, (168, 184, 214)
		)
		self.screen.blit(speed_text, (WINDOW_WIDTH - 240, 46))

		if self.finished:
			state_text = self.small_font.render("Sorted", True, (124, 245, 145))
		elif self.playing:
			state_text = self.small_font.render("Running", True, (255, 210, 120))
		else:
			state_text = self.small_font.render("Paused", True, (230, 230, 230))
		self.screen.blit(state_text, (WINDOW_WIDTH - 140, 16))

		chart_width = WINDOW_WIDTH - (2 * SIDE_MARGIN)
		bar_width = max(3, (chart_width - (len(self.values) - 1) * BAR_GAP) // len(self.values))

		max_value = max(self.values) if self.values else 1
		usable_height = WINDOW_HEIGHT - TOP_MARGIN - 30

		x = SIDE_MARGIN
		for idx, value in enumerate(self.values):
			# Scale each bar to the available vertical space.
			bar_height = int((value / max_value) * usable_height)
			y = WINDOW_HEIGHT - bar_height - 20

			color = (92, 136, 255)
			if self.sorted_from is not None and idx >= self.sorted_from:
				color = (74, 201, 120)
			if idx == self.active_left or idx == self.active_right:
				color = (255, 114, 94)

			pygame.draw.rect(self.screen, color, (x, y, bar_width, bar_height), border_radius=3)
			x += bar_width + BAR_GAP

		pygame.display.flip()

	def run(self) -> None:
		while self.running:
			self.handle_events()
			self.advance_sort()
			self.draw()
			self.clock.tick(60)

		pygame.quit()


if __name__ == "__main__":
	BubbleSortVisualizer().run()
