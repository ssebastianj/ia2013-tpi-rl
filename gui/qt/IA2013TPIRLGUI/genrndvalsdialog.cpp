#include "genrndvalsdialog.h"
#include "ui_genrndvalsdialog.h"

GenRndValsDialog::GenRndValsDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::GenRndValsDialog)
{
    ui->setupUi(this);
}

GenRndValsDialog::~GenRndValsDialog()
{
    delete ui;
}

void GenRndValsDialog::changeEvent(QEvent *e)
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
