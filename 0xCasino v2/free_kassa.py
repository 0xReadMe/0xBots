from hashlib import md5
from freekassa import FreeKassaApi
from config import FREE_KASSA_SECOND_SECRET, admins
from random import SystemRandom


class FreeKassa:
    def __init__(self, first_secret, second_secret, merchant_id, wallet_id) -> None:
        self.client = FreeKassaApi(
            first_secret=first_secret,
            second_secret=second_secret,
            merchant_id=merchant_id,
            wallet_id=wallet_id,
        )

    def get_payment_link(self, user_id: int, amount: float) -> str:
        return self.client.generate_payment_link(order_id=user_id, summ=float(amount))


if __name__ == "__main__":
    from flask import Flask, request
    from hashlib import md5
    from datetime import datetime
    from db import Logs, Global

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def hello_world():
        response = dict(request.args)

        amount = response.get("AMOUNT")

        user_id = response.get("MERCHANT_ORDER_ID")

        merchant_id = response.get("MERCHANT_ID")

        cur_id = response.get("CUR_ID")

        sign = response.get("SIGN")

        _sign = md5(
            f"{merchant_id}:{amount}:{FREE_KASSA_SECOND_SECRET}:{user_id}".encode(
                "utf-8"
            )
        ).hexdigest()

        if not (sign == _sign):
            return "", 400

        additional_information = "\n".join(
            [f"{key} : {value}" for key, value in dict(request.args).items()]
        )

        if not cur_id or cur_id != "45":
            message = f"[{datetime.now()}] WARNING: Кто-то пытался оплатить другой валютой\n\n{additional_information}\n\n"
            Logs.create(user_id=admins[0], message=message)
            return "", 200

        try:
            c = (
                Global.update(balance=Global.balance + amount)
                .where(Global.user_id == user_id)
                .execute()
            )

            with open("free-kassa-logs.txt", "a") as file:
                if c == 0:
                    message = f"[{datetime.now()}] ERROR: Не удалось выдать баланс, пользователь не найден!\n\n{additional_information}\n\n"
                    file.write(message)
                    Logs.create(user_id=admins[0], message=message)
                else:
                    message = f"[{datetime.now()}] RESULT: Успешно начислен баланс пользователю id{user_id} в размере {amount}\n\n{additional_information}\n\n"
                    file.write(message)
                    Logs.create(
                        user_id=user_id,
                        message=f"""✅ Ваш баланс пополнен на {amount} RUB
💰 Метод оплаты: Free-Kassa

💛 Приятной игры!""",
                    )
                    Logs.create(
                        user_id=admins[0],
                        message=f"""💸 Поступил платёж!
💰 Метод оплаты: Free-Kassa

{additional_information}""",
                    )

        except Exception as error:
            with open("free-kassa-logs.txt", "a") as file:
                message = (
                    f"[{datetime.now()}] ERROR: {error}\n\n{additional_information}\n\n"
                )
                file.write(message)
                Logs.create(user_id=admins[0], message=message)

        return "ok", 200

    print("RUNNED")
    app.run(debug=False, host="0.0.0.0", port=41632)
