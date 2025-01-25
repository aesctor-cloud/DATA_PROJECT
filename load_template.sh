# Espera a que NiFi esté listo
until $(curl --output /dev/null --silent --head --fail -u admin:ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB https://localhost:8443/nifi-api/flow/about); do
    sleep 5
done

# Sube el template al grupo raíz de NiFi
curl -X POST -F "template=@/opt/nifi/nifi-current/conf/Dataproject1-nifi.2.xml" \
    -u admin:ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB \
    https://localhost:8443/nifi-api/process-groups/root/templates/upload