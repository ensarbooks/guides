# Step-by-Step Guide: Spring Boot Dependency License Scanner

## 1. Project Setup

To start, create a new Spring Boot project using Maven. You can use [Spring Initializr](https://start.spring.io) or manually define a `pom.xml`. Ensure the project has the Spring Boot parent and necessary dependencies. For example, a minimal `pom.xml` might include:

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.1.3</version> <!-- use the latest Spring Boot version -->
</parent>

<groupId>com.example</groupId>
<artifactId>license-demo</artifactId>
<version>1.0.0</version>
<packaging>jar</packaging>

<dependencies>
    <!-- Spring Boot starter dependency (e.g., web if you plan a REST endpoint) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <!-- (Other dependencies can be added here) -->
</dependencies>
```

In the above, the Spring Boot parent provides default plugin configurations and dependency management. We include `spring-boot-starter-web` for a simple web application (optional if you only need a CLI app). After defining the POM, use your IDE or Maven to create the project structure (`src/main/java`, etc.), and add a basic Spring Boot application class:

```java
@SpringBootApplication
public class LicenseDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(LicenseDemoApplication.class, args);
    }
}
```

This ensures the Spring Boot app can start. At this point, you have a standard Spring Boot Maven project. We will now integrate license scanning tools into this project.

## 2. License Scanning Tool Integration

Next, integrate a license scanning tool to automatically extract open-source license information from the project’s dependencies. Maven artifacts often declare their license in their POM files ([dependencies - How To find the license and dependency version used in a maven project? - Stack Overflow](https://stackoverflow.com/questions/32510841/how-to-find-the-license-and-dependency-version-used-in-a-maven-project#:~:text=Reference%2C%20Dependencies%20maven)), so we can leverage plugins to gather that info instead of checking manually. Popular options include:

- **MojoHaus License Maven Plugin** – A Maven plugin to collect dependency licenses, generate reports, and even download license files.
- **SPDX Maven Plugin** – Generates an SPDX document (Software Package Data Exchange) listing all project artifacts and their licenses ([GitHub - spdx/spdx-maven-plugin: Plugin for supporting SPDX in a Maven build.](https://github.com/spdx/spdx-maven-plugin#:~:text=SPDX%20Maven%20Plugin%20is%20a,described%20in%20the%20POM%20file)), which is useful for compliance and SBOM generation.
- **ClearlyDefined (Eclipse Dash License Tool)** – Uses a curated database of open-source components to identify licenses. The Eclipse Dash License Tool has a Maven plugin (`license-check` goal) that fetches verified license data for all dependencies ([Eclipse Dash License Tool Maven Plugin | Wayne Beaton](http://blog.waynebeaton.ca/posts/ip/dash-license-tool-maven-plugin/#:~:text=Use%20the%20%60org.eclipse.dash%3Alicense,run%20the%20tool)).

For this guide, we’ll use the **License Maven Plugin** from MojoHaus, as it directly processes Maven dependencies. Add the plugin to your `pom.xml` in the build plugins section:

```xml
<build>
  <plugins>
    <!-- Plugin to scan and collect third-party licenses -->
    <plugin>
      <groupId>org.codehaus.mojo</groupId>
      <artifactId>license-maven-plugin</artifactId>
      <version>2.5.0</version>
      <executions>
        <execution>
          <id>download-licenses</id>
          <goals>
            <goal>download-licenses</goal>
          </goals>
          <!-- (Optional configuration can go here) -->
        </execution>
      </executions>
    </plugin>
    <!-- Spring Boot Maven plugin for packaging (already included via parent) -->
    <plugin>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-maven-plugin</artifactId>
    </plugin>
  </plugins>
</build>
```

In this configuration, we bind the `license:download-licenses` goal to the Maven build. When you package the project, this goal will scan all project dependencies, resolve their license information from their POMs, and download the corresponding license files. The plugin generates a **summary XML file** listing each dependency and its license(s) ([Download Licenses Examples – License Maven Plugin](https://www.mojohaus.org/license-maven-plugin/examples/example-download-licenses.html#:~:text=After%20downloading%20the%20license%20files%2C,forceDownload%20is%20set%20to%20true)). By default, license files and the summary XML are saved to `target/generated-resources/licenses` ([Download Licenses Examples – License Maven Plugin](https://www.mojohaus.org/license-maven-plugin/examples/example-download-licenses.html#:~:text=mvn%20package)).

> **Note:** The summary file (`licenses.xml`) includes entries for each dependency with the license name and URL. For example, an entry might look like:
>
> ```xml
> <dependency>
>   <groupId>org.slf4j</groupId>
>   <artifactId>jcl-over-slf4j</artifactId>
>   <licenses>
>     <license>
>       <name>MIT License</name>
>       <url>http://opensource.org/licenses/mit-license.php</url>
>     </license>
>   </licenses>
> </dependency>
> ```

After adding the plugin, you can also configure it as needed. For instance, you might specify a list of **allowed licenses** and fail the build if any dependency has an unapproved license ([Checking third party licenses | Strictly Typed blog](https://www.strictlytyped.com/checking-third-party-licenses/#:~:text=We%20can%20configure%20this%20plugin,not%20belong%20to%20this%20list)). (We’ll discuss compliance policies in step 6.) For now, we’ll use the default configuration which gathers all licenses without filtering.

If you prefer using SPDX, you could alternatively add the SPDX Maven Plugin. For example, binding the `spdx:createSPDX` goal will produce an SPDX bill-of-materials file enumerating all dependencies and their license identifiers ([GitHub - spdx/spdx-maven-plugin: Plugin for supporting SPDX in a Maven build.](https://github.com/spdx/spdx-maven-plugin#:~:text=%3C%21,%3C%2Fconfiguration%3E%20%3C%2Fplugin)). Similarly, to leverage ClearlyDefined data, you might run the Eclipse Dash License Tool plugin via a command like `mvn org.eclipse.dash:license-tool-maven:license-check`, which generates a `DEPENDENCIES` summary file and reports any unknown licenses ([Eclipse Dash License Tool Maven Plugin | Wayne Beaton](http://blog.waynebeaton.ca/posts/ip/dash-license-tool-maven-plugin/#:~:text=Use%20the%20%60org.eclipse.dash%3Alicense,run%20the%20tool)). These alternatives can be used in place of or alongside the License Maven Plugin, but for simplicity we will proceed with the MojoHaus plugin workflow.

## 3. Implementation Steps (Processing License Data)

With the license plugin integrated, the next step is to process the collected license information in our Spring Boot application. We want the app to identify and display the open-source licenses of its dependencies, using the data gathered by the plugin.

First, run the Maven build to ensure the license data is generated (more on this in the testing section). The `license-maven-plugin` will produce a file `licenses.xml` under `target/generated-resources/licenses`. This XML contains all dependencies and their license details as shown above. Our application can load this file at runtime and present the information.

We can implement a component that reads and parses `licenses.xml` on startup. For example, create a Spring `CommandLineRunner` bean that runs at application start and processes the XML:

```java
@Component
public class LicenseInfoRunner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        File xmlFile = new File("target/generated-resources/licenses/licenses.xml");
        // Parse the XML document
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = builder.parse(xmlFile);
        NodeList deps = doc.getElementsByTagName("dependency");
        // Iterate over dependencies
        for (int i = 0; i < deps.getLength(); i++) {
            Element dep = (Element) deps.item(i);
            String groupId = dep.getElementsByTagName("groupId").item(0).getTextContent();
            String artifactId = dep.getElementsByTagName("artifactId").item(0).getTextContent();
            NodeList licenses = dep.getElementsByTagName("license");
            // Each dependency can have multiple licenses
            for (int j = 0; j < licenses.getLength(); j++) {
                Element lic = (Element) licenses.item(j);
                String name = lic.getElementsByTagName("name").item(0).getTextContent();
                String url = lic.getElementsByTagName("url").item(0).getTextContent();
                // Display or store the license info
                System.out.println(groupId + ":" + artifactId + " - " + name + " (" + url + ")");
            }
        }
    }
}
```

In this code, we locate the `licenses.xml` file (generated by the Maven plugin) and use an XML parser to read its content. For each `<dependency>`, we retrieve the `groupId` and `artifactId`, then iterate through any `<license>` entries, extracting the license name and URL. We then print them to the console.

Instead of printing, you could store these details in a data structure to use elsewhere in the application. For instance, you might expose a REST endpoint (since we included Spring Web) that returns a JSON list of dependencies and licenses. In that case, you could map the XML data to a DTO (data transfer object) and return it via a controller. The approach above keeps it simple by just logging the information at startup.

**Key Point:** By using the Maven plugin’s output, we avoid hard-coding any license information. The application will always reflect whatever dependencies are present in the Maven POM. If you add or remove a dependency, regenerating the `licenses.xml` will update what the app displays. (If you run the app without updating the license data, it may show stale or incomplete info, so make sure to regenerate after dependency changes.)

## 4. Testing and Running the Application

Now that we have set up license scanning and implemented the code to display license details, it’s time to test the application:

1. **Build the Project**: Run `mvn clean package`. This triggers the license plugin during the build. You should see log output from the plugin as it resolves licenses (it may download license texts and produce the summary XML). After a successful build, check `target/generated-resources/licenses/` – you should find `licenses.xml` and possibly a folder of license text files.
2. **Run the Application**: Start the Spring Boot app. You can do this with `mvn spring-boot:run` (note: ensure the plugin ran by doing a package phase first if using this command) or by running the packaged jar: `java -jar target/license-demo-1.0.0.jar`.
3. **Verify Output**: Once the application starts, look at the console or log output. The `LicenseInfoRunner` should have printed each dependency with its license. For example, you might see lines like:

   ```text
   org.slf4j:jcl-over-slf4j - MIT License (http://opensource.org/licenses/mit-license.php)
   commons-logging:commons-logging - The Apache Software License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.txt)
   org.springframework.boot:spring-boot-starter-web - Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.txt)
   ```

   This confirms that the application has identified the open-source licenses for its dependencies. If you set up a REST endpoint instead, you would call that endpoint (e.g. `GET /licenses`) and verify the returned data structure contains the expected license entries.

4. **Testing Edge Cases**: Test what happens if a dependency has multiple licenses or if a license is missing. Our simple implementation prints all licenses declared. If a dependency had no license info in its POM, the `licenses.xml` entry might be empty or missing that dependency. The MojoHaus plugin usually flags such cases, so check the build log for warnings about missing license info. You can then supply manual info via the plugin configuration (using a `licensesConfigFile` as described in the plugin docs) to fill in the gaps ([Download Licenses Examples – License Maven Plugin](https://www.mojohaus.org/license-maven-plugin/examples/example-download-licenses.html#:~:text=By%20default%20the%20plugin%20will,following%20is%20an%20example%20license)).

By the end of this step, you should have a running Spring Boot application that, upon launch (or via an endpoint), lists all project dependencies and their associated license information.

## 5. Generating Reports (Formatting & Exporting License Info)

Having the license data is useful, but you may want to format it into user-friendly reports or export it for compliance records. There are several ways to generate reports from the collected license info:

- **Plain Text or Markdown**: The License Maven Plugin can generate a simple text summary of third-party licenses. Using the `license:add-third-party` goal will create a `THIRD-PARTY.txt` file in the build output that lists each dependency and its license. This file is often included in distributions. For example, a snippet of such a file might read:

  ```text
  List of 2 third-party dependencies.

   (The Apache Software License, Version 2.0) Commons Logging (commons-logging:commons-logging:1.1.1 - http://commons.apache.org/logging)
  ```

  This shows the license name in parentheses followed by the library name, coordinates, and homepage ([Thirdparty Licenses Examples – License Maven Plugin](https://www.mojohaus.org/license-maven-plugin/examples/example-thirdparty.html#:~:text=List%20of%202%20third)). You can customize the format using a FreeMarker template if needed (the plugin allows a custom `fileTemplate` for the third-party report).

- **HTML Report**: Maven’s Site plugin can be configured with License Maven Plugin to produce an HTML page of dependency licenses. For instance, binding the `license:aggregate-add-third-party` goal to the Maven site phase will include a nicely formatted table in the generated site (`mvn site`). This HTML can be shared with stakeholders or included in project documentation.

- **CSV or JSON Export**: If you prefer a machine-readable list (for feeding into another system or for auditing), you can use the XML (`licenses.xml`) we generated and transform it. Since our Spring Boot code already parses this XML, you could easily convert the collected data into JSON (using Jackson) or CSV. For example, you could write out a CSV with columns for _GroupId_, _ArtifactId_, _License Name_, _License URL_. This can be done in the `CommandLineRunner` or via a separate utility class.

- **SPDX SBOM**: As mentioned, the SPDX Maven Plugin can output an SPDX document ([GitHub - spdx/spdx-maven-plugin: Plugin for supporting SPDX in a Maven build.](https://github.com/spdx/spdx-maven-plugin#:~:text=SPDX%20Maven%20Plugin%20is%20a,described%20in%20the%20POM%20file)) ([GitHub - spdx/spdx-maven-plugin: Plugin for supporting SPDX in a Maven build.](https://github.com/spdx/spdx-maven-plugin#:~:text=%3C%21,%3C%2Fconfiguration%3E%20%3C%2Fplugin)) (e.g., `target/site/myproject-1.0.0.spdx`). SPDX is an industry-standard format for software bill-of-materials, containing detailed license info. Using SPDX format is beneficial if you need to integrate with compliance tools or produce an **SBOM** for regulations. Once generated, the SPDX file itself serves as a comprehensive report. You can also use tools from the SPDX community to convert that file into human-readable reports (HTML, PDF, etc., if needed).

- **Including License Texts**: The `download-licenses` goal already fetched the full license texts for each dependency (stored under `target/generated-resources/licenses`). For full compliance, especially when distributing software, you might package these license files into your application. One approach is to copy them into `src/main/resources` (or configure the plugin’s `licensesOutputDirectory` to point to `src/main/resources/licenses`) so that they get included in the JAR. Then you could, for example, have an "About" page or endpoint in your app that displays the license text of a selected dependency when needed. This ensures you are providing the actual license terms as required by some licenses.

Choose the format that best fits your needs. For quick internal checks, a console output or CSV might suffice. For official or user-facing documentation, an HTML page or included text file is more accessible. The key is that our build process has automated the extraction of license data, so generating any of these formats is straightforward by transforming the same source information.

## 6. Deployment Considerations and License Compliance Best Practices

Identifying licenses is not a one-time task – it’s an ongoing responsibility throughout your project’s lifecycle. Here are some best practices and considerations for maintaining open-source license compliance in a production environment:

- **Continuous Integration Checks**: Integrate license scanning into your CI/CD pipeline. Configure the build to **fail on disallowed licenses**. For example, you can maintain a whitelist (allowed licenses) and use the License Maven Plugin’s rules to fail the build if a dependency has a license outside the approved list ([Checking third party licenses | Strictly Typed blog](https://www.strictlytyped.com/checking-third-party-licenses/#:~:text=We%20can%20configure%20this%20plugin,not%20belong%20to%20this%20list)). This proactive step catches problematic licenses before the code is deployed. As one guide notes, “make the build fail if one of the libraries does not belong to [the allowed] list” ([Checking third party licenses | Strictly Typed blog](https://www.strictlytyped.com/checking-third-party-licenses/#:~:text=We%20can%20configure%20this%20plugin,not%20belong%20to%20this%20list)) – this ensures any issue gets immediate attention. A failed build due to license non-compliance should be treated with high priority.

- **Policy and Approval**: Establish a clear open-source usage policy. Decide which licenses are acceptable for your project (e.g., Apache 2.0, MIT might be allowed, while GPL might be restricted due to its stronger copyleft requirements ([Checking third party licenses | Strictly Typed blog](https://www.strictlytyped.com/checking-third-party-licenses/#:~:text=Some%20open%20source%20licenses%20are,same%20license%20as%20the%20library))). Communicate this policy to your development team so they can choose dependencies wisely. If a new library with a new license is needed, have a review process in place.

- **Maintain an Updated Inventory**: Keep an up-to-date inventory of third-party components and their licenses for each release of your application. Each time you update dependencies, re-run the license scan and update the reports. Version control your license documents (e.g., keep the `THIRD-PARTY.txt` or SPDX file in the repository or an artifact store). This historical record helps track license changes over time, and you can diff the reports between releases to see what changed.

- **Include Notices in Distribution**: Many open-source licenses (Apache 2.0, BSD, etc.) require that you include the license text and copyright notice in any distribution of your software. When deploying to production (especially if you distribute binaries to customers), bundle a copy of each required license. For a Spring Boot app, that could mean including a licenses directory in the packaged jar or alongside your distribution package. The files downloaded by the plugin can be used for this purpose. Also, if you have an “About” dialog or page, listing the third-party libraries and licenses there is a good practice (similar to Chrome’s `chrome://credits` page or Firefox’s `about:license` page which list all included OSS licenses).

- **Periodic Audits**: In addition to automated checks, consider doing a manual or tool-assisted audit periodically. Tools like the Eclipse Dash License Tool (ClearlyDefined) can cross-verify license info against a curated database, catching cases where POM data might be incomplete. For example, the Dash tool can confirm if all content has “vetted license information” and highlight anything that needs review ([Eclipse Dash License Tool Maven Plugin | Wayne Beaton](http://blog.waynebeaton.ca/posts/ip/dash-license-tool-maven-plugin/#:~:text=%5BINFO%5D%20,core%2FDEPENDENCIES%20%5BINFO%5D)). External auditing tools (FOSSA, Black Duck, etc.) can also be integrated for a more thorough analysis, especially for large projects.

- **Stay Informed**: Keep an eye on changes in the open-source licenses landscape. If a dependency changes its license in a newer version, that could impact your compliance. Also, be aware of security patches – sometimes you must upgrade a library for security reasons, and that might introduce a new license; ensure to scan after upgrades. Having license scanning as part of your release checklist will mitigate surprises.

By following these practices, your Spring Boot application will not only identify open-source licenses for its dependencies but also remain compliant with those licenses as it evolves. Automating license detection and integrating it into your development workflow helps avoid legal risks (since open-source licenses are legally binding agreements ([All You Need to Know About Open Source License Compliance](https://finitestate.io/blog/open-source-license-compliance#:~:text=Open%20source%20licenses%20are%20still,legal%20action%20and%20monetary%20damages))) and ensures you respect the open-source community by properly acknowledging and adhering to their license requirements.

---

By completing the steps above, you have developed a Spring Boot application that can list the open-source licenses of its dependencies, using Maven to automate license discovery. You’ve integrated a license scanning tool, processed the results in your code, and generated human-readable output. Going forward, you can refine this process (e.g., exporting in different formats or tightening compliance rules) and confidently manage open-source licenses in your project’s production deployments.
