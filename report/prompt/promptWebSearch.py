def prompt_web_search(html_content):
    return """You are a web content expert with a deep understanding of the HTML structure and its semantic meaning.You will be provided with the HTML code complete with a web page.Your task is to analyze it in detail and provide a complete and structured description of its content.Follow these guidelines in your analysis:

        General structure:

        Identify and describe the general structure of the page (Header, Nav, Main, Footer, etc.).
        It highlights any main divisions of the content (sections, articles, aside, etc.).


        Textual content:

        Analyze the text on the page, including securities, paragraphs, lists and other textual elements.
        Identify the main theme and attracts of the page.
        It highlights any keywords or important phrases.


        Multimedia content:

        Describe all the images present, including the content of the alt attribute if available.
        Report the presence of videos, audio or other built -in multimedia elements.


        Connections and navigation:

        Analyze the navigation structure of the page (menu, Broadcrumb, etc.).
        It lists the main internal and external connections, specifying their destination if deductible.


        Interactive elements:

        Identify and describe any form, buttons, or other interactive elements.
        Explains the aim and functionality of these elements.


        Metadata:

        Extract and analyze the metadata present in the document lead (title, Meta Description, Meta Keywords, etc.).
        Support them only in the following format Json: Metadati = {"Title": Title, "Metadescription": Meta Description, "Metikeywords": Meta Keywords, "Canonical": Canonical URL, "Ogtitle": OG TITLE, "OGDESCING": OG Description, "Ogimage": Og Image}.
        Evaluate their consistency with the actual content of the page.


        Semantics and accessibility:

        Evaluate the use of semantic HTML elements and their impact on the content structure.
        Comment on the accessibility of the page based on the use of air attributes, text alternatives, etc.


        Style and presentation:

        Briefly describe the visual aspect of the page based on any CSS classes or inline styles.
        It highlights particular or recurring design elements.


        Dynamic scripts and functionality:

        Identify the presence of scripts and briefly describe their possible features.


        Summary and evaluation:

        Provide a general synthesis of the content and purpose of the page.
        Offer a critical evaluation of the quality and effectiveness of the structure and content.



        Remember to be detailed but concise, focusing on the most relevant and significant elements of the page.Organize your analysis in clear sections and use focused or numbered lists to improve readability.If you notice unusual or problematic aspects, highlight them in your analysis.

        The HTML code of the web page is provided below: """ +html_content
        