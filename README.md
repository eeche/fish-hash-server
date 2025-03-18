# FISH-HASH-SERVER

If the hash verification server is on the same host, an attacker could gain access to the host and modify the hash value, thereby bypassing the verification process.  
To address this, it's safer to use a central management server and have the verification process handled independently from the host.  
This ensures the integrity of the verification process and prevents local tampering.

&nbsp;

해시 검증 서버가 동일한 호스트에 있으면, 공격자가 해당 호스트에 침입하여 해시값을 변조할 수 있어 검증을 우회할 수 있다.  
이를 해결하려면, 중앙 관리 서버를 두고, 검증 작업을 외부에서 독립적으로 처리하도록 해야한다.
