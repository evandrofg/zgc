FROM --platform=arm64 registry.access.redhat.com/ubi9/openjdk-21:latest

ENV LANGUAGE='en_US:en'

USER root

ENV CUSTOM_JDK_PATH=/usr/lib/jvm/zgc-openjdk

# Copy your custom JDK build to the Docker container
COPY build/linux-aarch64-server-release $CUSTOM_JDK_PATH

# Run alternatives commands
RUN alternatives --install /usr/bin/java java $CUSTOM_JDK_PATH/jdk/bin/java 20000 \
 && alternatives --install /usr/bin/javac javac $CUSTOM_JDK_PATH/jdk/bin/javac 20000 \
 && alternatives --set java $CUSTOM_JDK_PATH/jdk/bin/java \
 && alternatives --set javac $CUSTOM_JDK_PATH/jdk/bin/javac

 RUN microdnf install -y python3-psutil


# We make four distinct layers so if there are application changes the library layers can be re-used
# COPY --chown=185 target/quarkus-app/lib/ /deployments/lib/
# COPY --chown=185 target/quarkus-app/*.jar /deployments/
# COPY --chown=185 target/quarkus-app/app/ /deployments/app/
# COPY --chown=185 target/quarkus-app/quarkus/ /deployments/quarkus/

# EXPOSE 8080
USER 185

# ENV QUARKUS_VERTX_MAX_EVENT_LOOP_EXECUTE_TIME=30S

# ENV JAVA_OPTS="-Dorg.jooq.no-tips=true -Djava.security.egd=file:/dev/urandom -Dquarkus.http.host=0.0.0.0 -Djava.util.logging.manager=org.jboss.logmanager.LogManager"
# ENV JAVA_APP_JAR="/deployments/quarkus-run.jar"

# Set default command to /bin/bash
CMD ["/bin/bash"]
