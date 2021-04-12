; Hello world without C libs; uses Getstdhandle and writefile
; via the windows api
;
; written in the Intel asm style (destination before source)
;
; How-to
;   nasm -fwin32 hello.asm
;   link /subsystem:console /nodefaultlib /entry:main hello.obj
;

    global _main
    extern  _GetStdHandle@4
    extern  _WriteFile@20
    extern  _ExitProcess@4

    section .text
_main:
    ; DWORD  bytes;
    mov     ebp, esp                    ; move stack pointer to ebp
    sub     esp, 4                      ; allocate 4 bytes on the stack;

    ; hStdOut = GetstdHandle( STD_OUTPUT_HANDLE)
    push    -11                         ; stdout is DWORD -11
    call    _GetStdHandle@4             ; call api func
    mov     ebx, eax                    ; store the result of getstdhandle into ebx

    ; WriteFile( hstdOut, message, length(message), &bytes, 0);
    push    0                           ; set lpOverlapped to 0
    lea     eax, [ebp-4]                ; load effective address of DWORD bytes
    push    eax                         ;   and push to stack
    push    (message_end - message)     ; push the length onto the stack
    push    message                     ; push the message onto the stack
    push    ebx                         ; push hstdOut onto the stack
    call    _WriteFile@20               ; call api func

    ; ExitProcess(0)
    push    0                           ; exit with error code 0
    call    _ExitProcess@4              ; call api func

    ; never here
    hlt                                 ; halt if exitProcess were to fail for any reason
message:
    db      'Hello, World', 10
message_end:
