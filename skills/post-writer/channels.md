# Channel reference

What each channel takes: the hard character limit, how much shows before the fold, which formatting
works, and the hashtag and link conventions. Every number was read on the platform's own help or
developer pages on 2026-11-11, with the source next to it. Where the platform publishes no number,
the entry says `not documented by the platform` and names the secondary source used instead.

The hard limits here equal `skills/slop-check/rules/channels.json`. The checker counts characters as
Python does (one per Unicode code point); X and Threads count some characters differently (see their
notes), so leave a margin of a few characters near the limit there.

The hashtag maximums in `channels.json` (linkedin 5, x 2, threads 1, telegram 3, newsletter 0) are
conventions chosen for byline, not platform limits, except where a platform page says otherwise
(Threads, below). Byline posts end without a row of hashtags whatever the maximum.

## linkedin

| | |
|---|---|
| Hard limit | 3,000 characters per post. Source: https://www.linkedin.com/help/linkedin/answer/a528176 ("Posts can contain up to 3,000 characters"), read 2026-11-11. |
| Before the fold | Not documented by the platform. Secondary source: https://linkedinpreview.com/blog/linkedin-see-more-cutoff-2026 (dated 2026-06-14, read 2026-11-11) gives roughly the first 140 to 200 characters, cut earlier by line breaks. Write as if only the first two lines are seen. |
| Formatting | Plain text with line breaks and emoji. The help page lists no bold, italics or headings for posts. |
| Hashtags | Convention, not a platform limit: byline allows up to 5; the help page sets no number. |
| Links | A link in the text is allowed. No number is documented. |

## x

| | |
|---|---|
| Hard limit | 280 characters for a standard post. Source: https://docs.x.com/fundamentals/counting-characters.md, read 2026-11-11. Each URL counts as 23 characters whatever its length; each emoji counts as 2; Chinese, Japanese and Korean characters count as 2. |
| Before the fold | A post of 280 characters or fewer shows in full. |
| Formatting | Plain text with line breaks. |
| Hashtags | Convention, not a platform limit: byline allows up to 2. |
| Links | A link costs 23 characters of the 280 (source above). |

## threads

| | |
|---|---|
| Hard limit | 500 characters per post. Source: https://developers.facebook.com/documentation/threads/posts ("Text posts are limited to 500 characters"), read 2026-11-11. Emoji count as their number of UTF-8 bytes (same source), so an emoji can use up to 4 of the 500. |
| Text attachment | A text-only post can carry an attachment of up to 10,000 characters. Source: https://developers.facebook.com/documentation/threads/create-posts/text-attachments, read 2026-11-11. Byline writes the 500-character post; mention the attachment only if the person asks for a longer piece. |
| Before the fold | A post of 500 characters or fewer shows in full. Not documented by the platform for attachments. |
| Formatting | Plain text in the post. The attachment supports bold, italic, highlight, underline and strikethrough (attachment source above). |
| Hashtags | One topic tag per post: "Only one topic tag is allowed per post" (posts source above). This matches byline's maximum of 1. |
| Links | At most 5 links per post; the first URL becomes the link preview (posts source above). |

## telegram

| | |
|---|---|
| Hard limit | 4,096 characters per text message. Source: https://core.telegram.org/bots/api/methods/sendmessage.md ("1-4096 characters after entities parsing"), read 2026-11-11. A caption under a photo or video is shorter; keep a post with media as a text message. |
| Before the fold | A text message shows in full in the channel. Not documented by the platform as a number. |
| Formatting | Bold, italic, underline, strikethrough, spoiler, blockquote, code and text links. Source: https://core.telegram.org/bots/api (MessageEntity types), read 2026-11-11. |
| Hashtags | Convention, not a platform limit: byline allows up to 3. In a channel, tapping a hashtag shows the other posts with it (https://telegram.org/tour/channels), so a tag works as navigation inside the channel. |
| Links | No number documented. A link in the text is allowed. |

## newsletter

| | |
|---|---|
| Hard limit | None: there is no single platform. `char_limit` is `null`. Each sending tool has its own rules. |
| Before the fold | `not documented by the platform` (there is no single platform). Secondary source: Litmus, https://www.litmus.com/blog/the-ultimate-guide-to-preview-text-support (read 2026-11-11), advises keeping the preview text under 90 characters because inboxes show anywhere from none to a few lines. The first sentence is what the inbox shows. |
| Formatting | Whatever the sending tool supports: headings, bold, links and lists usually work. |
| Hashtags | None (maximum 0). |
| Links | Convention: as many as the text needs, each with words that say where it goes. |
