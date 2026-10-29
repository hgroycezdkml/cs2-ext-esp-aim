// Low-level mouse input helper used by the aim handler when smooth is disabled.
#include <windows.h>
#include <cmath>

extern "C" __declspec(dllexport)
void move_mouse_relative(int dx, int dy) {
    INPUT input = {0};
    input.type = INPUT_MOUSE;
    input.mi.dx = dx;
    input.mi.dy = dy;
    input.mi.dwFlags = MOUSEEVENTF_MOVE;
    SendInput(1, &input, sizeof(INPUT));
}