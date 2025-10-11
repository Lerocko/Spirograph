# test_spirograph.py
import pytest
from unittest import mock
import os
from spirograph_generator import generate_points, answer_yes_no, get_user_input, draw_spirograph, save_spirofig

# -----------------------------
# Test generate_points
# -----------------------------
def test_generate_points_default():
    xs, ys, scale_factor = generate_points()
    assert isinstance(xs, list)
    assert isinstance(ys, list)
    assert isinstance(scale_factor, int)
    assert len(xs) == len(ys)
    assert len(xs) > 0  # there should be points

def test_generate_points_custom():
    xs, ys, scale_factor = generate_points(100, 40, 30)
    assert all(isinstance(x, float) for x in xs)
    assert all(isinstance(y, float) for y in ys)
    assert len(xs) == len(ys)

# -----------------------------
# Test answer_yes_no
# -----------------------------
@mock.patch('builtins.input', side_effect=['y'])
def test_answer_yes_yes(mock_input):
    assert answer_yes_no("Prompt") == True

@mock.patch('builtins.input', side_effect=['n'])
def test_answer_no(mock_input):
    assert answer_yes_no("Prompt") == False

@mock.patch('builtins.input', side_effect=['yes'])
def test_answer_yes_text(mock_input):
    assert answer_yes_no("Prompt") == True

@mock.patch('builtins.input', side_effect=['no'])
def test_answer_no_text(mock_input):
    assert answer_yes_no("Prompt") == False

# Test invalid input looping until valid
@mock.patch('builtins.input', side_effect=['maybe', 'y'])
def test_answer_invalid_then_yes(mock_input):
    assert answer_yes_no("Prompt") == True

# -----------------------------
# Test get_user_input
# -----------------------------
@mock.patch('builtins.input', side_effect=['10', '5', '2'])
def test_get_user_input_valid(mock_input):
    R, r, d = get_user_input()
    assert R == 10
    assert r == 5
    assert d == 2

@mock.patch('builtins.input', side_effect=['-1', '5', '2', '10', '5', '2'])
def test_get_user_input_negative_then_valid(mock_input):
    R, r, d = get_user_input()
    assert R == 10
    assert r == 5
    assert d == 2

# -----------------------------
# Test draw_spirograph
# -----------------------------
def test_draw_spirograph_runs():
    xs, ys, scale_factor = generate_points(50, 20, 10)
    fig = draw_spirograph(xs, ys, scale_factor)
    assert fig is not None

# -----------------------------
# Test save_spirofig
# -----------------------------
@mock.patch('builtins.input', side_effect=['test_spiro.png'])
def test_save_spirofig_runs(mock_input):
    xs, ys, scale_factor = generate_points(50, 20, 10)
    fig = draw_spirograph(xs, ys, scale_factor)
    save_spirofig(fig)
    # Check that file was created
    assert os.path.exists('test_spiro.png')
    # Cleanup
    os.remove('test_spiro.png')
