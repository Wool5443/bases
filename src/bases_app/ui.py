"""GTK UI for the base converter."""

from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio, Gtk

from .converter import (
    ConversionError,
    MAX_SOURCE_BASE,
    MAX_TARGET_BASE,
    MIN_BASE,
    convert_number,
)


class BaseConverterWindow(Gtk.ApplicationWindow):
    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(application=app, title="Base Converter")
        self.set_default_size(520, 420)

        self.input_entry = Gtk.Entry(placeholder_text="Enter a number, e.g. 1011 or 1A")
        self.source_base = Gtk.SpinButton.new_with_range(MIN_BASE, MAX_SOURCE_BASE, 1)
        self.target_base = Gtk.SpinButton.new_with_range(MIN_BASE, MAX_TARGET_BASE, 1)
        self.source_base.set_value(10)
        self.target_base.set_value(2)

        self.error_label = Gtk.Label(xalign=0)
        self.error_label.add_css_class("error")
        self.error_label.set_wrap(True)

        self.string_output = Gtk.Entry(editable=False)
        self.digits_output = Gtk.Entry(editable=False)
        for entry in (self.input_entry, self.string_output, self.digits_output):
            entry.set_hexpand(True)
            entry.set_halign(Gtk.Align.FILL)
            entry.set_width_chars(1)

        self._build_ui()
        self._connect_signals()
        self.update_outputs()

    def _build_ui(self) -> None:
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        outer.set_hexpand(True)
        outer.set_margin_top(18)
        outer.set_margin_bottom(18)
        outer.set_margin_start(18)
        outer.set_margin_end(18)

        header = Gtk.Label(xalign=0)
        header.set_markup("<span size='x-large' weight='bold'>Convert Between Bases</span>")
        subtitle = Gtk.Label(
            label="Source bases 2 through 36, target bases 2 through 10000.",
            xalign=0,
        )
        subtitle.add_css_class("dim-label")

        grid = Gtk.Grid(column_spacing=12, row_spacing=12)
        grid.set_hexpand(True)
        grid.attach(Gtk.Label(label="Number", xalign=0), 0, 0, 1, 1)
        grid.attach(self.input_entry, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label="Source base", xalign=0), 0, 1, 1, 1)
        grid.attach(self.source_base, 1, 1, 1, 1)
        grid.attach(Gtk.Label(label="Target base", xalign=0), 0, 2, 1, 1)
        grid.attach(self.target_base, 1, 2, 1, 1)

        convert_button = Gtk.Button(label="Convert")
        convert_button.connect("clicked", self._on_convert_clicked)

        results = Gtk.Frame(label="Results")
        results.set_hexpand(True)
        results_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        results_box.set_hexpand(True)
        results_box.set_margin_top(12)
        results_box.set_margin_bottom(12)
        results_box.set_margin_start(12)
        results_box.set_margin_end(12)

        results_grid = Gtk.Grid(column_spacing=12, row_spacing=12)
        results_grid.set_hexpand(True)
        results_grid.attach(Gtk.Label(label="String output", xalign=0), 0, 0, 1, 1)
        results_grid.attach(self.string_output, 1, 0, 1, 1)
        results_grid.attach(Gtk.Label(label="Digit values", xalign=0), 0, 1, 1, 1)
        results_grid.attach(self.digits_output, 1, 1, 1, 1)
        results_box.append(results_grid)
        results.set_child(results_box)

        outer.append(header)
        outer.append(subtitle)
        outer.append(grid)
        outer.append(convert_button)
        outer.append(self.error_label)
        outer.append(results)

        self.set_child(outer)

    def _connect_signals(self) -> None:
        self.input_entry.connect("changed", self._on_input_changed)
        self.source_base.connect("value-changed", self._on_input_changed)
        self.target_base.connect("value-changed", self._on_input_changed)

    def _on_input_changed(self, *_args: object) -> None:
        self.update_outputs()

    def _on_convert_clicked(self, _button: Gtk.Button) -> None:
        self.update_outputs()

    def update_outputs(self) -> None:
        try:
            result = convert_number(
                self.input_entry.get_text(),
                self.source_base.get_value_as_int(),
                self.target_base.get_value_as_int(),
            )
        except ConversionError as exc:
            self.error_label.set_text(str(exc))
            self.string_output.set_text("")
            self.digits_output.set_text("")
            return

        self.error_label.set_text("")
        self.string_output.set_text(result.text)
        self.digits_output.set_text(str(result.digits))


class BaseConverterApp(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="com.example.bases", flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self) -> None:
        window = self.props.active_window
        if window is None:
            window = BaseConverterWindow(self)
        window.present()
