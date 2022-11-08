import re
import html

from slack_bolt.workflows.step import WorkflowStep

class CustomWorkflowStep:
    def __init__(self):
        self.id_extract_pattern = re.compile("<[#@]([^>]+)>")

    def register(self, app, callback_id):
        ws = WorkflowStep(
            callback_id=callback_id,
            edit=self.edit,
            save=self.save,
            execute=[self.ack, self.execute],
        )
        app.step(ws)
    
    def edit(self, ack, step, configure, logger):
        ack()
        logger.info(step)

        blocks = [
            {
                "type": "input",
                "block_id": "message_input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "message",
                    "placeholder": {"type": "plain_text", "text": "メッセージを入力します"},
                    "initial_value": step.get("inputs", {}).get("message", {}).get("value", ""),
                },
                "label": {"type": "plain_text", "text": "ポストするメッセージの内容"},
            },            
            {   # 「投稿先チャンネル」入力欄
                "type": "input",
                "block_id": "channelid_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "channelid",
                    "placeholder": {"type": "plain_text", "text": "変数より、ワークフローを開始したチャンネル、を選択してください"},
                    "initial_value": step.get("inputs", {}).get("channelid", {}).get("value", ""),
                },
                "label": {"type": "plain_text", "text":"メッセージを表示するチャンネル"},
            },
            {   # 「対象ユーザ」入力欄
                "type": "input",
                "block_id": "userid_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "userid",
                    "placeholder": {"type": "plain_text", "text":"変数より、「XXX」をクリックしたユーザー（メンション）、を選択してください"},
                    "initial_value": step.get("inputs", {}).get("userid", {}).get("value", ""),
                },
                "label": {"type": "plain_text", "text":"メッセージを表示するユーザ"},
            },
        ]
        configure(blocks=blocks)
    
    def save(self, ack, body, view, update, logger):
        ack()
        logger.info(body)

        values = view["state"]["values"]

        inputs = {
            "message": {"value": values["message_input"]["message"]["value"]},
            "channelid": {"value": values["channelid_input"]["channelid"]["value"]},
            "userid": {"value": values["userid_input"]["userid"]["value"]},
        }
        update(inputs=inputs, outputs=[])
    
    def execute(self, body, client, step, complete, fail, logger):
        logger.info(body)

        inputs = step["inputs"]

        # ユーザID
        m = self.id_extract_pattern.search(inputs["userid"]["value"])
        userid = m.group(1) if m else None
        
        # チャンネルID
        m = self.id_extract_pattern.search(inputs["channelid"]["value"])
        channelid = m.group(1) if m else None

        if userid is None or channelid is None:
            message = f"ユーザID もしくは チャンネルID の指定が不適切です。userid: {userid}, channeldid: {channelid}"
            logger.error(message)
            fail(error={"message": message})
            return
        logger.info(f"userid: {userid}, channeldid: {channelid}")

        client.chat_postEphemeral(
            channel=channelid,
            user=userid,
            text='',
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": html.unescape(inputs["message"]["value"]),
                    },
                },
            ]
        )

        complete(outputs={})

    def ack(self, ack, logger):
        logger.info("ack")
        ack()
