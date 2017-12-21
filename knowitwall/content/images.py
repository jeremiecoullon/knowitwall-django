import bs4 as bs

def wrap(to_wrap, wrap_in):
    contents = to_wrap.replace_with(wrap_in)
    wrap_in.append(contents)

def create_transcript_image(input_html):
    """
    Take transcript and check if any of the images have a 'le_image_middle' or
    'le_image_left' as one of their classes. If so, wrap them in the correct tags.

    Parameters
    ---------
    input_html: str
        Transcript as html

    Returns
    -------
    New html transcript as a string
    """
    bs_transcript = bs.BeautifulSoup(input_html, 'html.parser')

    for img_tag in bs_transcript.findAll("img"):

        if img_tag.has_attr("class"):
            image_type = img_tag['class'][0]
        else:
            continue

        if image_type=='le_image_middle':
            image_class = "tr_image_middle"
            figure_class = "figure_transcript_middle"
        elif image_type =="le_image_left":
            image_class = "tr_image_left"
            figure_class = "figure_transcript_left"
        else:
            continue

        img_src = img_tag.attrs['src']
        if img_tag.has_attr("longdesc"):
            img_desc = img_tag.attrs['longdesc']
        else:
            img_desc = ""

        img_tag.attrs['class']=image_class
        img_tag.attrs['style']=""
        new_figure_tag = bs_transcript.new_tag("figure", **{'class': figure_class})
        new_anchor_tag = bs_transcript.new_tag("a", **{'class':'fancybox_transcript', 'href': img_src,
                                                       'title': img_desc})

        new_figcaption_tag = bs_transcript.new_tag("figcaption")
        new_figcaption_tag.string = img_desc
        wrap(img_tag, new_figure_tag)
        img_tag.insert_after(new_figcaption_tag)
        wrap(img_tag, new_anchor_tag)
    return str(bs_transcript)
