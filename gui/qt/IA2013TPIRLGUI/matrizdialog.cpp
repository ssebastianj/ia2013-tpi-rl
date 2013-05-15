#include "matrizdialog.h"
#include "ui_matrizdialog.h"

MatrizDialog::MatrizDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::MatrizDialog)
{
    ui->setupUi(this);
}

MatrizDialog::~MatrizDialog()
{
    delete ui;
}

void MatrizDialog::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
}
