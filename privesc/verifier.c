#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);

    printf("NeonVerify System Integrity Checker v1.0\n");
    printf("Verifying system logs...\n");

    // VULNERABILITY: Relative path usage in system()
    // Attackers can create a file named 'cat' in a directory they control,
    // add that directory to their PATH, and this binary will execute their 'cat'
    // with root privileges.
    int result = system("cat /var/log/neon_verify.log 2>/dev/null || echo 'Log file not found.'");

    if (result == 0) {
        printf("System integrity verified.\n");
    } else {
        printf("System integrity check failed.\n");
    }

    return 0;
}
